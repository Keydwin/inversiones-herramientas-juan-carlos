from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Proveedor

supplier_blueprint = Blueprint('proveedores', __name__)

@supplier_blueprint.route('/proveedores', methods=['GET'])
def query_suppliers():
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        proveedores = Proveedor.query.filter(Proveedor.NombreProveedor.ilike(f'%{search_query}%')).all()
        if not proveedores:
            flash('Proveedor no encontrado', 'warning')
    else:
        proveedores = Proveedor.query.all()
        
    return render_template('supplier.html', supplier=proveedores, search_query=search_query)

@supplier_blueprint.route('/proveedores/register', methods=['POST'])
def register_supplier():
    nombre = request.form.get('NombreProveedor')

    if not nombre:
        flash('El nombre del proveedor es obligatorio', 'error')
        return redirect(url_for('proveedores.query_suppliers'))
    
    nuevo_proveedor = Proveedor(NombreProveedor=nombre)
    db.session.add(nuevo_proveedor)
    db.session.commit()
    
    flash('Proveedor registrado exitosamente', 'success')
    return redirect(url_for('proveedores.query_suppliers'))

@supplier_blueprint.route('/proveedores/modificar/<int:id>', methods=['GET', 'POST'])
def modify_supplier(id):
    proveedor = Proveedor.query.get_or_404(id)
    
    if request.method == 'POST':
        nuevo_nombre = request.form.get('NombreProveedor')
        if nuevo_nombre:
            proveedor.NombreProveedor = nuevo_nombre
            db.session.commit()
            flash('Proveedor modificado exitosamente', 'success')
            return redirect(url_for('proveedores.query_suppliers'))
        
    return render_template('modificar_proveedor.html', proveedor=proveedor)

@supplier_blueprint.route('/proveedores/delete/<int:id>', methods=['POST'])
def delete_supplier(id):
    proveedor = Proveedor.query.get_or_404(id)
    
    db.session.delete(proveedor)
    db.session.commit()
    
    flash('Proveedor eliminado exitosamente', 'success')
    return redirect(url_for('proveedores.query_suppliers'))

@supplier_blueprint.route('/proveedores/report', methods=['GET'])
def generate_supplier_report():
    flash('Generando reporte...', 'info')
    return redirect(url_for('proveedores.query_suppliers'))