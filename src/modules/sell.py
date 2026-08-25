from flask import Blueprint, render_template, request, make_response, current_app, flash, redirect, url_for, session
from models import db, Venta, Cliente, Persona, ProductoVenta, Producto, Usuario, Estado, Parroquia, Municipio, Inventario, Trabajador
from sqlalchemy.orm import joinedload
from datetime import datetime
import io, os
from xhtml2pdf import pisa

sell_blueprint = Blueprint('sell', __name__)

# List all sales with optional date filtering and pagination
@sell_blueprint.route('/ventas', methods=['GET'])
def query_sales():
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query_ventas = Venta.query.options(
        joinedload(Venta.productoventa).joinedload(ProductoVenta.producto),
        joinedload(Venta.cliente).joinedload(Cliente.persona)
    ).order_by(Venta.IdVenta.desc())

    if start_date:
        query_ventas = query_ventas.filter(Venta.FechaVenta >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query_ventas = query_ventas.filter(Venta.FechaVenta <= datetime.strptime(end_date, '%Y-%m-%d').date())

    pagination = query_ventas.paginate(page=page, per_page=10, error_out=False)

    productos = Producto.query.all()
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    return render_template('sell.html', pagination=pagination, productos=productos, fecha_actual=fecha_actual, start_date=start_date, end_date=end_date)


# Search and select a client for a new sale
@sell_blueprint.route('/ventas/cliente', methods=['GET'])
def select_client_page():
    page = request.args.get('page_cli', 1, type=int)
    search_cli = request.args.get('search_cli', '', type=str)

    query_cli = Cliente.query.join(Persona).options(
        joinedload(Cliente.persona),
        joinedload(Cliente.parroquia)
            .joinedload(Parroquia.municipio)
            .joinedload(Municipio.estado)
    ).order_by(Persona.Nombre.asc())

    if search_cli:
        query_cli = query_cli.filter(
            (Persona.Nombre.ilike(f'%{search_cli}%')) | 
            (Persona.Apellido.ilike(f'%{search_cli}%')) |
            (Persona.Cedula.cast(db.String).ilike(f'%{search_cli}%'))
        )

    clientes_pagination = query_cli.paginate(page=page, per_page=11, error_out=False)

    return render_template('select_client.html', clientes_pagination=clientes_pagination, search_cli=search_cli)


# Store selected client in session and go to product selection
@sell_blueprint.route('/ventas/seleccionar-cliente/<int:id_cliente>', methods=['POST'])
def save_client_session(id_cliente):
    cli = Cliente.query.options(joinedload(Cliente.persona)).get_or_404(id_cliente)
    session['venta_id_cliente'] = cli.IdCliente
    session['venta_nombre_cliente'] = f"{cli.persona.Nombre} {cli.persona.Apellido}"
    return redirect(url_for('sell.register_sale_page'))


# Render form to select products for the sale
@sell_blueprint.route('/ventas/productos', methods=['GET'])
def register_sale_page():
    id_cliente = session.get('venta_id_cliente')
    nombre_cliente = session.get('venta_nombre_cliente')

    if not id_cliente:
        flash('Por favor seleccione un cliente primero.', 'danger')
        return redirect(url_for('sell.select_client_page'))

    productos = Producto.query.all()
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    return render_template('register_sale.html', id_cliente=id_cliente, nombre_cliente=nombre_cliente, productos=productos, fecha_actual=fecha_actual)


# Process sale, insert items, and update stock
@sell_blueprint.route('/save_sale', methods=['POST'])
def save_sale():
    try:
        id_cliente = session.get('venta_id_cliente')
        id_trabajador = session.get('id_trabajador') 

        if not id_trabajador:
            flash('Error de sesión: No se identificó al trabajador. Inicie sesión nuevamente.', 'danger')
            return redirect(url_for('login.login'))

        if not id_cliente:
            flash('Seleccione un cliente para realizar la venta.', 'danger')
            return redirect(url_for('sell.select_client_page'))

        fecha = request.form.get('Fecha')
        monto_total = float(request.form.get('MontoTotal', 0))
        metodo_pago = request.form.get('TipoPago')

        # Get product IDs and quantities from form submission
        ids_productos = request.form.getlist('id_producto[]')
        cantidades = request.form.getlist('cantidad[]')

        # Check if products were submitted
        if not ids_productos or not cantidades:
            flash('Debe agregar al menos un producto a la venta.', 'danger')
            return redirect(url_for('sell.register_sale_page'))

        # Check stock availability before saving
        for id_prod_str, cant_str in zip(ids_productos, cantidades):
            id_prod = int(id_prod_str)
            cantidad = int(cant_str)

            inv = Inventario.query.filter_by(IdProducto=id_prod).first()
            prod = Producto.query.get(id_prod)
            nombre = prod.NombreProducto if prod else f"ID {id_prod}"

            stock_actual = inv.CantidadProducto if inv else 0

            if stock_actual < cantidad:
                flash(f'Stock insuficiente para el producto "{nombre}". Disponible: {stock_actual}, Solicitado: {cantidad}.', 'danger')
                return redirect(url_for('sell.register_sale_page'))

        # Save sale header
        nueva_venta = Venta(
            IdTrabajador=id_trabajador,
            IdCliente=id_cliente,
            FechaVenta=datetime.strptime(fecha, '%Y-%m-%d').date(),
            MetodoPago=metodo_pago,
            MontoTotal=monto_total
        )
        db.session.add(nueva_venta)
        db.session.flush() # Get new sale ID

        # Save sale details and update inventory stock
        for id_prod_str, cant_str in zip(ids_productos, cantidades):
            id_prod = int(id_prod_str)
            cantidad = int(cant_str)

            producto = Producto.query.get(id_prod)

            if metodo_pago in ['Crédito', 'Credito']:
                precio_unitario = float(producto.PrecioCredito)
            else:
                precio_unitario = float(producto.PrecioDeContado)

            subtotal = cantidad * precio_unitario

            # Create sale detail row
            detalle = ProductoVenta(
                IdVenta=nueva_venta.IdVenta,
                IdProducto=id_prod,
                Cantidad=cantidad,
                PrecioUnitario=precio_unitario,
                Subtotal=subtotal
            )
            db.session.add(detalle)

            # Subtract quantity from inventory
            inv = Inventario.query.filter_by(IdProducto=id_prod).first()
            if inv:
                inv.CantidadProducto -= cantidad

        db.session.commit()

        # Clear client data from session
        session.pop('venta_id_cliente', None)
        session.pop('venta_nombre_cliente', None)

        flash('Venta registrada exitosamente y stock actualizado.', 'success')
        return redirect(url_for('sell.query_sales'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar la venta: {str(e)}', 'danger')
        return redirect(url_for('sell.register_sale_page'))


# Generate general sales PDF report
@sell_blueprint.route('/ventas/sell_report')
def generate_sell_report():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query_ventas = Venta.query.options(
        joinedload(Venta.cliente).joinedload(Cliente.persona)
    ).order_by(Venta.FechaVenta.asc())
    
    if start_date:
        query_ventas = query_ventas.filter(Venta.FechaVenta >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query_ventas = query_ventas.filter(Venta.FechaVenta <= datetime.strptime(end_date, '%Y-%m-%d').date())

    ventas = query_ventas.all()
    ruta_static = os.path.join(current_app.root_path, 'static')
    
    html_renderizado = render_template('pdf_sell.html', ventas=ventas, base_dir=ruta_static)
    output_memoria = io.BytesIO()
    
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)
    
    if pisa_status.err:
        return "Error al generar el PDF", 500
        
    output_memoria.seek(0)
    
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_ventas.pdf'
    
    return response


# Generate personal sales PDF report for current worker
@sell_blueprint.route('/ventas/seller_report')
def generate_seller_report():
    id_trabajador = session.get('id_trabajador')

    if not id_trabajador:
        flash('Debe iniciar sesión para generar su reporte personal.', 'danger')
        return redirect(url_for('login.login'))

    trabajador = Trabajador.query.options(joinedload(Trabajador.persona)).get(id_trabajador)

    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query_ventas = Venta.query.options(
        joinedload(Venta.cliente).joinedload(Cliente.persona)
    ).filter(Venta.IdTrabajador == id_trabajador).order_by(Venta.FechaVenta.asc())

    if start_date:
        query_ventas = query_ventas.filter(Venta.FechaVenta >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query_ventas = query_ventas.filter(Venta.FechaVenta <= datetime.strptime(end_date, '%Y-%m-%d').date())

    ventas = query_ventas.all()
    ruta_static = os.path.join(current_app.root_path, 'static')

    # Render template with worker and sales data
    html_renderizado = render_template('pdf_seller.html', ventas=ventas, trabajador=trabajador, base_dir=ruta_static)
    output_memoria = io.BytesIO()
    
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)
    
    if pisa_status.err:
        return "Error al generar el PDF del vendedor", 500
        
    output_memoria.seek(0)
    
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_ventas_personales.pdf'
    
    return response