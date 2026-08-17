import calendar
from datetime import datetime, date
from flask import Blueprint, render_template, request
from sqlalchemy import func, desc

# Import based on your exact models.py file
from models import (db, Compra, ProductoCompra, Venta, ProductoVenta, Producto, Proveedor, Cliente, Persona, Trabajador)

stats_blueprint = Blueprint('stats', __name__)

@stats_blueprint.route('/estadisticas')
def view_statistics():

 # 1. Date Filters (Defaults to current month)

    start_date_str = request.args.get('start_date', '').strip()
    end_date_str = request.args.get('end_date', '').strip()
    cliente_id = request.args.get('client_id', type=int)
    proveedor_id = request.args.get('supplier_id', type=int)

    today = date.today()

    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = date(today.year, today.month, 1)
            start_date_str = start_date.strftime('%Y-%m-%d')
    else:
        start_date = date(today.year, today.month, 1)
        start_date_str = start_date.strftime('%Y-%m-%d')

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            last_day = calendar.monthrange(today.year, today.month)[1]
            end_date = date(today.year, today.month, last_day)
            end_date_str = end_date.strftime('%Y-%m-%d')
    else:
        last_day = calendar.monthrange(today.year, today.month)[1]
        end_date = date(today.year, today.month, last_day)
        end_date_str = end_date.strftime('%Y-%m-%d')

    clientes = Cliente.query.join(Persona).order_by(Persona.Nombre.asc(), Persona.Apellido.asc()).all()
    proveedores = Proveedor.query.order_by(Proveedor.NombreProveedor.asc()).all()


 # 2. Base Filtered Queries

    compras_q = db.session.query(Compra)
    ventas_q = db.session.query(Venta)

    if start_date:
        compras_q = compras_q.filter(Compra.Fecha >= start_date)
        ventas_q = ventas_q.filter(Venta.FechaVenta >= start_date)

    if end_date:
        compras_q = compras_q.filter(Compra.Fecha <= end_date)
        ventas_q = ventas_q.filter(Venta.FechaVenta <= end_date)

    if proveedor_id:
        compras_q = compras_q.filter(Compra.IdProveedor == proveedor_id)

    if cliente_id:
        ventas_q = ventas_q.filter(Venta.IdCliente == cliente_id)

    compras_subq = compras_q.with_entities(Compra.IdCompra).subquery()
    ventas_subq = ventas_q.with_entities(Venta.IdVenta).subquery()


# 3. General KPIs

    res_invertido = compras_q.with_entities(func.coalesce(func.sum(Compra.MontoTotal), 0)).scalar()
    res_ingresos = ventas_q.with_entities(func.coalesce(func.sum(Venta.MontoTotal), 0)).scalar()

    total_invertido = float(res_invertido or 0)
    total_ingresos = float(res_ingresos or 0)
    balance_general = total_ingresos - total_invertido

    res_unidades_compradas = db.session.query(
        func.coalesce(func.sum(ProductoCompra.Cantidad), 0)
    ).filter(ProductoCompra.IdCompra.in_(compras_subq)).scalar()

    res_unidades_vendidas = db.session.query(
        func.coalesce(func.sum(ProductoVenta.Cantidad), 0)
    ).filter(ProductoVenta.IdVenta.in_(ventas_subq)).scalar()

    total_unidades = int(res_unidades_compradas or 0)
    total_unidades_vendidas = int(res_unidades_vendidas or 0)

 # 4. Top 5 Most Purchased Products

    top_comprados = (
        db.session.query(
            Producto.NombreProducto,
            func.sum(ProductoCompra.Cantidad).label('cant')
        )
        .join(ProductoCompra, Producto.IdProducto == ProductoCompra.IdProducto)
        .filter(ProductoCompra.IdCompra.in_(compras_subq))
        .group_by(Producto.NombreProducto)
        .order_by(desc('cant'))
        .limit(5)
        .all()
    )
    prod_names = [p[0].strip() for p in top_comprados if p[0]]
    prodQtys = [int(p[1]) for p in top_comprados]


# 5. Top 5 Most Sold Products

    top_vendidos = (
        db.session.query(
            Producto.NombreProducto,
            func.sum(ProductoVenta.Cantidad).label('cant')
        )
        .join(ProductoVenta, Producto.IdProducto == ProductoVenta.IdProducto)
        .filter(ProductoVenta.IdVenta.in_(ventas_subq))
        .group_by(Producto.NombreProducto)
        .order_by(desc('cant'))
        .limit(5)
        .all()
    )
    sold_prod_names = [s[0].strip() for s in top_vendidos if s[0]]
    sold_prod_qtys = [int(s[1]) for s in top_vendidos]


# 6. Top 5 Suppliers

    top_proveedores = (
        db.session.query(
            Proveedor.NombreProveedor,
            func.sum(Compra.MontoTotal).label('monto_total')
        )
        .join(Compra, Proveedor.IdProveedor == Compra.IdProveedor)
        .filter(Compra.IdCompra.in_(compras_subq))
        .group_by(Proveedor.NombreProveedor)
        .order_by(desc('monto_total'))
        .limit(5)
        .all()
    )
    supplier_names = [p[0].strip() for p in top_proveedores if p[0]]
    supplier_totals = [float(p[1]) for p in top_proveedores]

    
# 7. Top 5 Clients

    top_clientes = (
        db.session.query(
            func.concat(Persona.Nombre, ' ', Persona.Apellido).label('nombre_completo'),
            func.sum(Venta.MontoTotal).label('monto_total')
        )
        .join(Cliente, Persona.IdPersona == Cliente.IdPersona)
        .join(Venta, Cliente.IdCliente == Venta.IdCliente)
        .filter(Venta.IdVenta.in_(ventas_subq))
        .group_by(Persona.IdPersona, Persona.Nombre, Persona.Apellido)
        .order_by(desc('monto_total'))
        .limit(5)
        .all()
    )
    client_names = [c[0].strip() for c in top_clientes if c[0]]
    client_totals = [float(c[1]) for c in top_clientes]


# 8. Top 5 Sellers (Workers)

    top_vendedores = (
        db.session.query(
            func.concat(Persona.Nombre, ' ', Persona.Apellido).label('nombre_completo'),
            func.sum(Venta.MontoTotal).label('monto_total')
        )
        .join(Trabajador, Persona.IdPersona == Trabajador.IdPersona)
        .join(Venta, Trabajador.IdTrabajador == Venta.IdTrabajador)
        .filter(Venta.IdVenta.in_(ventas_subq))
        .group_by(Persona.IdPersona, Persona.Nombre, Persona.Apellido)
        .order_by(desc('monto_total'))
        .limit(5)
        .all()
    )
    seller_names = [v[0].strip() for v in top_vendedores if v[0]]
    seller_totals = [float(v[1]) for v in top_vendedores]
    
    return render_template(
        'statistics.html',
        total_invertido=total_invertido,
        total_ingresos=total_ingresos,
        balance_general=balance_general,
        total_unidades=total_unidades,
        total_unidades_vendidas=total_unidades_vendidas,
        prod_names=prod_names,
        prodQtys=prodQtys,
        sold_prod_names=sold_prod_names,
        sold_prod_qtys=sold_prod_qtys,
        supplier_names=supplier_names,
        supplier_totals=supplier_totals,
        client_names=client_names,
        client_totals=client_totals,
        seller_names=seller_names,
        seller_totals=seller_totals,
        clients=clientes,
        suppliers=proveedores,
        start_date=start_date_str,
        end_date=end_date_str,
        selected_client=cliente_id,
        selected_supplier=proveedor_id
    )