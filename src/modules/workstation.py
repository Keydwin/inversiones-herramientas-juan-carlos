from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, PuestoTrabajo 
from sqlalchemy.exc import IntegrityError

workstation_blueprint = Blueprint('workstation', __name__)

@workstation_blueprint.route('/puestos', methods=['GET'])
def query_workstations():
    search_query = request.args.get('search')
    
    page = request.args.get('page', 1, type=int)
    per_page = 5 
    
    if search_query:
        paginacion = PuestoTrabajo.query.filter(PuestoTrabajo.NombrePuestoTrabajo.ilike(f'%{search_query}%')).paginate(page=page, per_page=per_page, error_out=False)
    else:
        paginacion = PuestoTrabajo.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('workstation.html', pagination=paginacion, search_query=search_query)

@workstation_blueprint.route('/workstation/register', methods=['POST'])
def register_workstation():
    if request.method == 'POST':
        nombre = request.form.get('Nombre')
        sueldo = request.form.get('Sueldo')

        if not nombre or not sueldo:
            flash('El nombre y el sueldo son obligatorios', 'error')
            return redirect(url_for('workstation.query_workstations'))
        
        nuevo_puesto = PuestoTrabajo(
            NombrePuestoTrabajo=nombre, 
            Sueldo=sueldo
        )
        db.session.add(nuevo_puesto)
        db.session.commit()
        
        flash('Puesto de trabajo registrado exitosamente', 'success')
        return redirect(url_for('workstation.query_workstations'))

@workstation_blueprint.route('/workstation/modificar/<int:id>', methods=['GET', 'POST'])
def modify_workstation(id):
    puesto = PuestoTrabajo.query.get_or_404(id)
    
    if request.method == 'POST':
        puesto.NombrePuestoTrabajo = request.form.get('Nombre')
        puesto.Sueldo = request.form.get('Sueldo')
        
        db.session.commit()
        flash('Puesto de trabajo modificado exitosamente', 'success')
        return redirect(url_for('workstation.query_workstations'))
        
    return render_template('modificar_puesto.html', puesto=puesto)

@workstation_blueprint.route('/workstation/eliminar/<int:id>', methods=['POST'])
def delete_workstation(id):
    puesto = PuestoTrabajo.query.get_or_404(id)
    
    try:
        db.session.delete(puesto)
        db.session.commit()
        flash('Puesto de trabajo eliminado exitosamente.', 'success')
        
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar: Hay trabajadores que tienen asignado este puesto.', 'error') # o 'danger', según tu CSS
        
    return redirect(url_for('workstation.query_workstations'))

@workstation_blueprint.route('/workstation/report', methods=['GET'])
def generate_workstations_report():
    puesto_filtro = request.args.get('puesto', '')
    
    if puesto_filtro:
        puestos_db = PuestoTrabajo.query.filter(PuestoTrabajo.NombrePuestoTrabajo.ilike(f'%{puesto_filtro}%')).all()
    else:
        puestos_db = PuestoTrabajo.query.all()

    return render_template('pdf_workstation.html', workstations=puestos_db, puesto_filtro=puesto_filtro)