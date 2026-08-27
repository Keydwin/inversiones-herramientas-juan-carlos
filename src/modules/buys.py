from flask import Blueprint, render_template, request, make_response, current_app, flash, redirect, url_for, session
from models import db, Compra, Proveedor, ProductoCompra, Producto, Inventario, LibroDiario
from sqlalchemy.orm import joinedload
from datetime import datetime
import io, os
from xhtml2pdf import pisa

buy_blueprint = Blueprint('buy', __name__)

# List purchases with date range filtering and pagination
@buy_blueprint.route('/compras', methods=['GET'])
def query_purchases():
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query_compras = Compra.query.options(
        joinedload(Compra.productocompra).joinedload(ProductoCompra.producto),
        joinedload(Compra.proveedor)
    ).order_by(Compra.IdCompra.desc())

    if start_date:
        query_compras = query_compras.filter(Compra.Fecha >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query_compras = query_compras.filter(Compra.Fecha <= datetime.strptime(end_date, '%Y-%m-%d').date())

    pagination = query_compras.paginate(page=page, per_page=10, error_out=False)

    productos = Producto.query.all()
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    return render_template('buy.html', pagination=pagination, productos=productos, fecha_actual=fecha_actual, start_date=start_date, end_date=end_date)


# Search and select a provider for a new purchase
@buy_blueprint.route('/compras/proveedor', methods=['GET'])
def select_provider_page():
    page = request.args.get('page_prov', 1, type=int)
    search_prov = request.args.get('search_prov', '', type=str)

    query_prov = Proveedor.query.order_by(Proveedor.NombreProveedor.asc())
    if search_prov:
        query_prov = query_prov.filter(Proveedor.NombreProveedor.ilike(f'%{search_prov}%'))

    proveedores_pagination = query_prov.paginate(page=page, per_page=11, error_out=False)

    return render_template('select_provider.html', proveedores_pagination=proveedores_pagination, search_prov=search_prov)


# Store selected provider in session and proceed to purchase form
@buy_blueprint.route('/compras/seleccionar-proveedor/<int:id_proveedor>', methods=['POST'])
def save_provider_session(id_proveedor):
    prov = Proveedor.query.get_or_404(id_proveedor)
    session['compra_id_proveedor'] = prov.IdProveedor
    session['compra_nombre_proveedor'] = prov.NombreProveedor
    return redirect(url_for('buy.register_purchase_page'))


# Render form to select products for the purchase
@buy_blueprint.route('/compras/productos', methods=['GET'])
def register_purchase_page():
    id_proveedor = session.get('compra_id_proveedor')
    nombre_proveedor = session.get('compra_nombre_proveedor')

    if not id_proveedor:
        flash('Por favor seleccione un proveedor primero.', 'danger')
        return redirect(url_for('buy.select_provider_page'))

    productos = Producto.query.all()
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    return render_template('register_purchase.html', id_proveedor=id_proveedor, nombre_proveedor=nombre_proveedor, productos=productos, fecha_actual=fecha_actual)


# Process purchase, update product prices, and increase inventory
@buy_blueprint.route('/compras/guardar', methods=['POST'])
def save_purchase_multi():
    try:
        id_proveedor = session.get('compra_id_proveedor')
        fecha_str = request.form.get('Fecha')
        monto_total = float(request.form.get('MontoTotal', 0))

        if not id_proveedor:
            flash('Sesión expirada. Vuelva a seleccionar el proveedor.', 'danger')
            return redirect(url_for('buy.select_provider_page'))

        # Check if at least one product was submitted in the form
        if 'productos[0][IdProducto]' not in request.form:
            flash('Debe agregar al menos un producto a la compra.', 'danger')
            return redirect(url_for('buy.register_purchase_page'))

        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        # Save purchase header
        nueva_compra = Compra(
            IdProveedor=int(id_proveedor),
            Fecha=fecha,
            MontoTotal=round(monto_total, 2)
        )
        db.session.add(nueva_compra)
        db.session.flush() # Generate new purchase ID

        # Loop through purchase line items
        index = 0
        while f'productos[{index}][IdProducto]' in request.form:
            id_producto = int(request.form.get(f'productos[{index}][IdProducto]'))
            cantidad = int(request.form.get(f'productos[{index}][Cantidad]', 0))
            costo_unitario = float(request.form.get(f'productos[{index}][CostoUnitario]', 0))
            subtotal = round(cantidad * costo_unitario, 2)

            prod = Producto.query.get(id_producto)

            # Determine cash and credit prices
            precio_contado_form = request.form.get(f'productos[{index}][PrecioDecontado]') or request.form.get(f'productos[{index}][PrecioDeContado]')
            precio_credito_form = request.form.get(f'productos[{index}][PrecioCredito]')

            if precio_contado_form and precio_credito_form:
                precio_de_contado = round(float(precio_contado_form), 2)
                precio_credito = round(float(precio_credito_form), 2)
            else:
                porc_contado = prod.PorcenajeDeContado if (prod and prod.PorcenajeDeContado) else 0
                porc_credito = prod.PorcentajeCredito if (prod and prod.PorcentajeCredito) else 0

                precio_de_contado = round(costo_unitario * (1 + (porc_contado / 100)), 2)
                precio_credito = round(costo_unitario * (1 + (porc_credito / 100)), 2)

            # 1. Add item detail to purchase
            detalle = ProductoCompra(
                IdCompra=nueva_compra.IdCompra,
                IdProducto=id_producto,
                Cantidad=cantidad,
                CostoUnitario=costo_unitario,
                Subtotal=subtotal
            )
            db.session.add(detalle)

            # 2. Increase inventory stock or create new record
            inv = Inventario.query.filter_by(IdProducto=id_producto).first()
            if inv:
                inv.CantidadProducto += cantidad
            else:
                nuevo_inventario = Inventario(
                    IdProducto=id_producto,
                    CantidadProducto=cantidad
                )
                db.session.add(nuevo_inventario)

            # 3. Update selling prices in product table
            if prod:
                prod.PrecioDeContado = precio_de_contado
                prod.PrecioCredito = precio_credito

            index += 1

            asiento_diario = LibroDiario(
            Fecha=fecha,
            Concepto=f"Compra de mercancía para inventario - Compra N° {nueva_compra.IdCompra}",
            Debe=round(monto_total, 2),
            IdCompra=nueva_compra.IdCompra
        )
        db.session.add(asiento_diario)

        db.session.commit()
        flash('Compra, inventario y asiento en Libro Diario registrados con éxito.', 'success')

        # Clear session data
        session.pop('compra_id_proveedor', None)
        session.pop('compra_nombre_proveedor', None)

        return redirect(url_for('buy.query_purchases'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar compra: {str(e)}', 'danger')
        return redirect(url_for('buy.register_purchase_page'))


# Generate purchases PDF report
@buy_blueprint.route('/compras/buy_report')
def generate_buy_report():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query_compras = Compra.query.options(
        joinedload(Compra.proveedor)
    ).order_by(Compra.Fecha.asc())
    
    if start_date:
        query_compras = query_compras.filter(Compra.Fecha >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query_compras = query_compras.filter(Compra.Fecha <= datetime.strptime(end_date, '%Y-%m-%d').date())

    compras = query_compras.all()
    ruta_static = os.path.join(current_app.root_path, 'static')
    
    html_renderizado = render_template('pdf_buy.html', compras=compras, base_dir=ruta_static)
    output_memoria = io.BytesIO()
    
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)
    
    if pisa_status.err:
        return "Error al generar el PDF", 500
        
    output_memoria.seek(0)
    
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_compras.pdf'
    
    return response