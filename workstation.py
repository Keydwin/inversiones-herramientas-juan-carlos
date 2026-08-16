from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, PuestoTrabajo 

workstation = Blueprint('workstation', __name__)

@workstation.route('/puestos', methods=['GET'])
def query_workstations():
    search_query = request.args.get('search')
    
    if search_query:
        puestos_db = PuestoTrabajo.query.filter(PuestoTrabajo.nombre.ilike(f'%{search_query}%')).all()
    else:
        puestos_db = PuestoTrabajo.query.all()

    return render_template('workstation.html', workstations=puestos_db, search_query=search_query)

@workstation.route('/workstation/register', methods=['POST'])
def register_workstation():
    if request.method == 'POST':
        nombre = request.form.get('Nombre')
        obligaciones = request.form.get('Obligaciones')
        sueldo = request.form.get('Sueldo')

        if not nombre or not obligaciones or not sueldo:
            flash('Todos los campos (nombre, obligaciones, sueldo) son obligatorios', 'error')
            return redirect(url_for('workstation.query_workstations'))
        
        nuevo_puesto = PuestoTrabajo(
            nombre=nombre, 
            obligaciones=obligaciones, 
            sueldo=sueldo
        )
        db.session.add(nuevo_puesto)
        db.session.commit()
        
        flash('Puesto de trabajo registrado exitosamente', 'success')
        return redirect(url_for('workstation.query_workstations'))

@workstation.route('/workstation/modificar/<int:id>', methods=['GET', 'POST'])
def modify_workstation(id):
    puesto = PuestoTrabajo.query.get_or_404(id)
    
    if request.method == 'POST':
        puesto.nombre = request.form.get('Nombre')
        puesto.obligaciones = request.form.get('Obligaciones')
        puesto.sueldo = request.form.get('Sueldo')
        
        db.session.commit()
        flash('Puesto de trabajo modificado exitosamente', 'success')
        return redirect(url_for('workstation.query_workstations'))
        
    return render_template('modificar_puesto.html', puesto=puesto)

@workstation.route('/workstation/eliminar/<int:id>', methods=['POST'])
def delete_workstation(id):
    puesto = PuestoTrabajo.query.get_or_404(id)
    
    db.session.delete(puesto)
    db.session.commit()
    
    flash('Puesto de trabajo eliminado exitosamente', 'success')
    return redirect(url_for('workstation.query_workstations'))