from flask import Blueprint, render_template, request, make_response, current_app, flash, redirect, url_for, session
from models import db, Compra, Proveedor, ProductoCompra, Producto
from sqlalchemy.orm import joinedload
from datetime import datetime
import io, os
from xhtml2pdf import pisa

buy_blueprint = Blueprint('buy', __name__)

@buy_blueprint.route('/compras', methods=['GET'])
def query_purchases():
    # 1. Parámetros para la tabla principal de Compras
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    # AGREGAMOS options(joinedload(...)) PARA TRAER PRODUCTOCOMPRA Y EL NOMBRE DEL PRODUCTO
    query_compras = Compra.query.options(
        joinedload(Compra.productocompra).joinedload(ProductoCompra.producto),
        joinedload(Compra.proveedor)
    ).order_by(Compra.IdCompra.desc())

    if start_date:
        query_compras = query_compras.filter(Compra.Fecha >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query_compras = query_compras.filter(Compra.Fecha <= datetime.strptime(end_date, '%Y-%m-%d').date())

    pagination = query_compras.paginate(page=page, per_page=10, error_out=False)


    # 3. Obtener catálogo de productos para el modal de registro paso 2
    productos = Producto.query.all()
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    return render_template(
        'buy.html',
        pagination=pagination,
        productos=productos,
        fecha_actual=fecha_actual,
        start_date=start_date,
        end_date=end_date,
    )


@buy_blueprint.route('/compras/nueva/proveedor', methods=['GET'])
def select_provider_page():
    page = request.args.get('page_prov', 1, type=int)
    search_prov = request.args.get('search_prov', '', type=str)

    query_prov = Proveedor.query.order_by(Proveedor.NombreProveedor.asc())
    if search_prov:
        query_prov = query_prov.filter(Proveedor.NombreProveedor.ilike(f'%{search_prov}%'))

    proveedores_pagination = query_prov.paginate(page=page, per_page=11, error_out=False)

    return render_template(
        'select_provider.html',
        proveedores_pagination=proveedores_pagination,
        search_prov=search_prov
    )


@buy_blueprint.route('/compras/nueva/seleccionar-proveedor/<int:id_proveedor>', methods=['POST'])
def save_provider_session(id_proveedor):
    # Guardamos en la sesión de Flask el proveedor seleccionado
    prov = Proveedor.query.get_or_404(id_proveedor)
    session['compra_id_proveedor'] = prov.IdProveedor
    session['compra_nombre_proveedor'] = prov.NombreProveedor
    return redirect(url_for('buy.register_purchase_page'))


@buy_blueprint.route('/compras/nueva/productos', methods=['GET'])
def register_purchase_page():
    # Validar que primero seleccionó un proveedor
    id_proveedor = session.get('compra_id_proveedor')
    nombre_proveedor = session.get('compra_nombre_proveedor')

    if not id_proveedor:
        flash('Por favor seleccione un proveedor primero.', 'warning')
        return redirect(url_for('buy.select_provider_page'))

    productos = Producto.query.all()
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    return render_template(
        'register_purchase.html',
        id_proveedor=id_proveedor,
        nombre_proveedor=nombre_proveedor,
        productos=productos,
        fecha_actual=fecha_actual
    )


@buy_blueprint.route('/compras/guardar', methods=['POST'])
def save_purchase_multi():
    try:
        id_proveedor = session.get('compra_id_proveedor')
        fecha_compra_str = request.form.get('fecha_compra')
        monto_total = float(request.form.get('monto_total', 0))

        if not id_proveedor:
            flash('Sesión expirada. Vuelva a seleccionar el proveedor.', 'danger')
            return redirect(url_for('buy.select_provider_page'))

        fecha_compra = datetime.strptime(fecha_compra_str, '%Y-%m-%d').date()

        # 1. Crear la cabecera de la Compra
        nueva_compra = Compra(
            IdProveedor=int(id_proveedor),
            Fecha=fecha_compra,
            MontoTotal=monto_total
        )
        db.session.add(nueva_compra)
        db.session.flush()

        # 2. Recorrer los detalles enviados
        index = 0
        while f'productos[{index}][id_producto]' in request.form:
            id_producto = int(request.form.get(f'productos[{index}][id_producto]'))
            cantidad = int(request.form.get(f'productos[{index}][cantidad]'))
            costo_unitario = float(request.form.get(f'productos[{index}][costo_unitario]'))
            porc_contado = float(request.form.get(f'productos[{index}][porc_contado]', 0))
            porc_credito = float(request.form.get(f'productos[{index}][porc_credito]', 0))

            subtotal = cantidad * costo_unitario

            # Crear detalle en ProductoCompra
            detalle = ProductoCompra(
                IdCompra=nueva_compra.IdCompra,
                IdProducto=id_producto,
                Cantidad=cantidad,
                CostoUnitario=costo_unitario,
                Subtotal=subtotal,
                PrecioDecontado=costo_unitario * (1 + (porc_contado / 100)),
                PrecioCredito=costo_unitario * (1 + (porc_credito / 100))
            )
            db.session.add(detalle)

            # Actualizar porcentajes y precios en catálogo base
            prod = Producto.query.get(id_producto)
            if prod:
                prod.PorcenajeDeContado = int(porc_contado)
                prod.PorcentajeCredito = int(porc_credito)
                prod.PrecioDeContado = costo_unitario * (1 + (porc_contado / 100))
                prod.PrecioCredito = costo_unitario * (1 + (porc_credito / 100))

            index += 1

        db.session.commit()

        # Limpiamos los datos temporales de la sesión
        session.pop('compra_id_proveedor', None)
        session.pop('compra_nombre_proveedor', None)

        flash('Compra registrada con éxito.', 'success')
        return redirect(url_for('buy.query_purchases'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar compra: {str(e)}', 'danger')
        return redirect(url_for('buy.register_purchase_page'))