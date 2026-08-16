from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Venta, Cliente, Producto, DetalleVenta

sales_blueprint = Blueprint('sales', __name__)

@sales_blueprint.route('/ventas', methods=['GET'])
def query_sales():
    search_query = request.args.get('q', '').strip()
    query = Venta.query

    if search_query:
        query = query.join(Cliente).filter(
            (Venta.id.like(f"%{search_query}%")) | 
            (Cliente.nombre.ilike(f"%{search_query}%"))
        )
    
    sales = query.all()
    message = "venta no encontrado" if not sales and search_query else None
    
    return render_template('sales_list.html', sales=sales, message=message, search_query=search_query)


@sales_blueprint.route('/mis-ventas', methods=['GET'])
@login_required
def my_sales():
    search_query = request.args.get('q', '').strip()
    query = Venta.query.filter_by(vendedor_id=current_user.id)

    if search_query:
        query = query.filter(Venta.id.like(f"%{search_query}%"))

    sales = query.all()
    message = "venta no encontrado" if not sales and search_query else None

    return render_template('my_sales.html', sales=sales, message=message, search_query=search_query)


@sales_blueprint.route('/ventas/nueva', methods=['GET', 'POST'])
@login_required
def register_sale():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        metodo_pago = request.form.get('metodo_pago') # 'contado' o 'crédito'
        producto_ids = request.form.getlist('producto_ids')
        cantidades = request.form.getlist('cantidades')

        nueva_venta = Venta(
            cliente_id=cliente_id,
            vendedor_id=current_user.id,
            metodo_pago=metodo_pago,
            fecha=datetime.now(),
            monto_total=0.0,
            estado_entrega='Pendiente'
        )
        db.session.add(nueva_venta)
        db.session.flush()

        monto_total = 0.0
        for p_id, cant_str in zip(producto_ids, cantidades):
            cantidad = int(cant_str)
            producto = Producto.query.get(p_id)
            
            if producto and producto.existencia >= cantidad:
                subtotal = producto.precio * cantidad
                monto_total += subtotal
                producto.existencia -= cantidad  # Descuenta stock

                detalle = DetalleVenta(
                    venta_id=nueva_venta.id,
                    producto_id=p_id,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                db.session.add(detalle)

        nueva_venta.monto_total = monto_total
        db.session.commit()
        flash("Venta registrada con éxito.", "success")
        return redirect(url_for('sales.query_sales'))

    clientes = Cliente.query.all()
    productos = Producto.query.filter(Producto.existencia > 0).all()
    return render_template('register_sale.html', clientes=clientes, productos=productos)


@sales_blueprint.route('/ventas/editar/<int:id>', methods=['GET', 'POST'])
def edit_sale(id):
    venta = Venta.query.get_or_404(id)

    if venta.estado_entrega == 'Entregado':
        flash("No se puede editar una venta que ya ha sido entregada.", "danger")
        return redirect(url_for('sales.query_sales'))

    if request.method == 'POST':
        venta.metodo_pago = request.form.get('metodo_pago', venta.metodo_pago)
        db.session.commit()
        flash("Datos de la venta actualizados correctamente.", "info")
        return redirect(url_for('sales.query_sales'))

    return render_template('edit_sale.html', venta=venta)