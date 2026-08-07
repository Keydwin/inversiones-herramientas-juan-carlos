from flask import Blueprint, render_template, request, make_response, current_app, flash, redirect, url_for, session
from models import db, Compra, Proveedor, ProductoCompra, Producto
from sqlalchemy.orm import joinedload
from datetime import datetime
import io, os
from xhtml2pdf import pisa

buy_blueprint = Blueprint('buy', __name__)

@buy_blueprint.route('/compras', methods=['GET'])
def query_purchases():
    #  Parámetros para la tabla principal de Compras
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


    #  Obtener catálogo de productos para el modal de registro paso 2
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
        #  Obtener datos de cabecera
        IdProveedor = session.get('compra_id_proveedor')
        Fecha_str = request.form.get('Fecha')
        MontoTotal = float(request.form.get('MontoTotal', 0))

        if not IdProveedor:
            flash('Sesión expirada. Vuelva a seleccionar el proveedor.', 'danger')
            return redirect(url_for('buy.select_provider_page'))

        Fecha = datetime.strptime(Fecha_str, '%Y-%m-%d').date()

        # Instancia de Compra
        nueva_compra = Compra(
            IdProveedor=int(IdProveedor),
            Fecha=Fecha,
            MontoTotal=round(MontoTotal, 2)
        )
        db.session.add(nueva_compra)
        db.session.flush()

        #  Recorrer los detalles enviados mediante indices de formulario
        index = 0
        while f'productos[{index}][IdProducto]' in request.form:
            IdProducto = int(request.form.get(f'productos[{index}][IdProducto]'))
            Cantidad = int(request.form.get(f'productos[{index}][Cantidad]'))
            CostoUnitario = float(request.form.get(f'productos[{index}][CostoUnitario]'))
            Subtotal = round(Cantidad * CostoUnitario, 2)

            prod = Producto.query.get(IdProducto)

            # Intentar obtener los precios calculados enviados desde el frontend JS
            precio_contado_form = request.form.get(f'productos[{index}][PrecioDecontado]') or request.form.get(f'productos[{index}][PrecioDeContado]')
            precio_credito_form = request.form.get(f'productos[{index}][PrecioCredito]')

            if precio_contado_form and precio_credito_form:
                PrecioDecontado = round(float(precio_contado_form), 2)
                PrecioCredito = round(float(precio_credito_form), 2)
            else:
                # Respaldo: Recalcular con porcentajes de la base de datos si no vienen en el POST
                porc_contado = prod.PorcenajeDeContado if (prod and hasattr(prod, 'PorcenajeDeContado') and prod.PorcenajeDeContado) else 0
                porc_credito = prod.PorcentajeCredito if (prod and hasattr(prod, 'PorcentajeCredito') and prod.PorcentajeCredito) else 0

                PrecioDecontado = round(CostoUnitario * (1 + (porc_contado / 100)), 2)
                PrecioCredito = round(CostoUnitario * (1 + (porc_credito / 100)), 2)

            # Instancia de ProductoCompra (Detalle de la compra)
            detalle = ProductoCompra(
                IdCompra=nueva_compra.IdCompra,
                IdProducto=IdProducto,
                Cantidad=Cantidad,
                CostoUnitario=CostoUnitario,
                Subtotal=Subtotal,
                PrecioDecontado=PrecioDecontado,
                PrecioCredito=PrecioCredito
            )
            db.session.add(detalle)

            # Actualizar precios catálogo en el modelo Producto
            if prod:
                if hasattr(prod, 'PrecioDecontado'):
                    prod.PrecioDecontado = PrecioDecontado
                elif hasattr(prod, 'PrecioDeContado'):
                    prod.PrecioDeContado = PrecioDecontado

                if hasattr(prod, 'PrecioCredito'):
                    prod.PrecioCredito = PrecioCredito

            index += 1

        db.session.commit()

        # Limpiar variables de sesión
        session.pop('compra_id_proveedor', None)
        session.pop('compra_nombre_proveedor', None)

        flash('Compra registrada con éxito.', 'success')
        return redirect(url_for('buy.query_purchases'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar compra: {str(e)}', 'danger')
        return redirect(url_for('buy.register_purchase_page'))