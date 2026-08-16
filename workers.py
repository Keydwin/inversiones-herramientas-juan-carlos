from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Trabajador, Puesto

trabajador = Blueprint('trabajador', __name__)

@trabajador.route('/trabajadores', methods=['GET'])
def query_workers():
    busqueda = request.args.get('busqueda', '').strip()
    
    if busqueda:
        trabajadores_db = Trabajador.query.filter(
            (Trabajador.nombre.ilike(f'%{busqueda}%')) |
            (Trabajador.apellido.ilike(f'%{busqueda}%')) |
            (Trabajador.cedula.ilike(f'%{busqueda}%'))
        ).all()
        
        if not trabajadores_db:
            flash('Trabajador no encontrado', 'error')
    else:
        trabajadores_db = Trabajador.query.all()
        
    puestos = Puesto.query.all()
    
    return render_template('trabajadores.html', trabajadores=trabajadores_db, puestos=puestos)

@trabajador.route('/trabajador/register', methods=['POST'])
def register_worker():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        puesto_id = request.form.get('puesto_id')

        if not nombre or not apellido or not cedula or not puesto_id:
            flash('El nombre, apellido, cédula y el puesto son obligatorios', 'error')
            return redirect(url_for('trabajador.query_workers'))
        
        nuevo_trabajador = Trabajador(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            telefono=telefono,
            correo=correo,
            puesto_id=puesto_id,
            estatus='activo'
        )
        db.session.add(nuevo_trabajador)
        db.session.commit()
        
        flash('Trabajador registrado exitosamente', 'success')
        return redirect(url_for('trabajador.query_workers'))

@trabajador.route('/trabajador/modificar/<int:id>', methods=['GET', 'POST'])
def modify_worker(id):
    trabajador_obj = Trabajador.query.get_or_404(id)
    puestos = Puesto.query.all()
    
    if request.method == 'POST':
        trabajador_obj.nombre = request.form.get('nombre')
        trabajador_obj.apellido = request.form.get('apellido')
        trabajador_obj.cedula = request.form.get('cedula')
        trabajador_obj.telefono = request.form.get('telefono')
        trabajador_obj.correo = request.form.get('correo')
        trabajador_obj.puesto_id = request.form.get('puesto_id')
        
        db.session.commit()
        flash('Datos del trabajador modificados exitosamente', 'success')
        return redirect(url_for('trabajador.query_workers'))
        
    return render_template('modificar_trabajador.html', trabajador=trabajador_obj, puestos=puestos)

@trabajador.route('/trabajador/eliminar/<int:id>', methods=['POST'])
def delete_worker(id):
    trabajador_obj = Trabajador.query.get_or_404(id)
    
    trabajador_obj.estatus = 'inactivo'
    db.session.commit()
    
    flash('Trabajador eliminado exitosamente', 'success')
    return redirect(url_for('trabajador.query_workers'))