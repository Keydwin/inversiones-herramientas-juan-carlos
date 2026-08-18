from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Trabajador, Persona, PuestoTrabajo

workers_blueprint = Blueprint('trabajador', __name__)

@workers_blueprint.route('/trabajadores', methods=['GET'])
def query_workers():
    busqueda = request.args.get('busqueda', '').strip()
    
    if busqueda:
        trabajadores_db = Trabajador.query.join(Persona).filter(
            (Persona.nombre.ilike(f'%{busqueda}%')) |
            (Persona.apellido.ilike(f'%{busqueda}%')) |
            (Persona.cedula.ilike(f'%{busqueda}%'))
            (Persona.Estatus == 'activo') | (Persona.estatus == 'activo')
        ).all()
        
        if not trabajadores_db:
            flash('Trabajador no encontrado', 'error')
    else:
        trabajadores_db = Trabajador.query.all()
        
    puestos = PuestoTrabajo.query.all()
    print("TOTAL DE PUESTOS ENCONTRADOS:", len(puestos))
    
    return render_template('workers.html', trabajadores=trabajadores_db, puestos=puestos)

@workers_blueprint.route('/trabajador/register', methods=['POST'])
def register_worker():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        cedula_raw = request.form.get('cedula')
        telefono_raw = request.form.get('telefono')
        correo = request.form.get('correo')
        idPuestoTrabajo = request.form.get('idPuestoTrabajo')
        sueldo = request.form.get('sueldo')

        # --- LÍNEAS DE DEBUGEO TEMPORALES ---
        print("--> ID DE PUESTO RECIBIDO DEL FORMULARIO:", idPuestoTrabajo)
        puestos_debug = PuestoTrabajo.query.all()
        for p in puestos_debug:
            print(f"Puesto en BD -> ID: {getattr(p, 'idPuestoTrabajo', getattr(p, 'IdPuestoTrabajo', 'N/A'))}")
        # ------------------------------------

        if not nombre or not apellido or not cedula_raw or not idPuestoTrabajo:
            flash('Todos los campos obligatorios deben ser llenados', 'error')
            return redirect(url_for('trabajador.query_workers'))
        
        try:
            cedula = int(cedula_raw.replace('.', '').replace(',', '').strip())
        except ValueError:
            flash('La cédula debe contener solo números', 'error')
            return redirect(url_for('trabajador.query_workers'))
        
        digits = ''.join(filter(str.isdigit, telefono_raw or ''))
        telefono = (int(digits) % 2000000000) if digits else 0

        nueva_persona = Persona()
        nueva_persona.Cedula = cedula
        nueva_persona.Nombre = nombre
        nueva_persona.Apellido = apellido
        nueva_persona.Telefono = telefono
        nueva_persona.Correo = correo
        nueva_persona.Estatus = 'activo'

        db.session.add(nueva_persona)
        db.session.commit() # Genera el IdPersona

        nuevo_trabajador = Trabajador()
        nuevo_trabajador.IdPersona = nueva_persona.IdPersona
        nuevo_trabajador.IdPuestoTrabajo = int(idPuestoTrabajo) if idPuestoTrabajo else None
        if hasattr(nuevo_trabajador, 'Sueldo'):
            nuevo_trabajador.Sueldo = sueldo.replace(',', '.') if sueldo else '0'
        else:
            nuevo_trabajador.sueldo = sueldo.replace(',', '.') if sueldo else '0'

        db.session.add(nuevo_trabajador)
        db.session.commit()
        
        flash('Trabajador registrado exitosamente', 'success')
        return redirect(url_for('trabajador.query_workers'))
        
@workers_blueprint.route('/trabajador/modificar/<int:id>', methods=['GET', 'POST'])
def modify_worker(id):
    trabajador_obj = Trabajador.query.get_or_404(id)
    puestos = PuestoTrabajo.query.all()
    
    if request.method == 'POST':
        persona = getattr(trabajador_obj, 'Persona', getattr(trabajador_obj, 'persona', None))
        if persona:
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            cedula_raw = request.form.get('cedula', '')
            telefono_raw = request.form.get('telefono', '')
            
            try:
                cedula = int(cedula_raw.replace('.', '').replace(',', '').strip()) if cedula_raw else 0
            except ValueError:
                cedula = 0
                
        digits = ''.join(filter(str.isdigit, telefono_raw or ''))
        telefono = (int(digits) % 2000000000) if digits else 0

        if hasattr(persona, 'Nombre'): persona.Nombre = nombre
        else: persona.nombre = nombre
            
        if hasattr(persona, 'Apellido'): persona.Apellido = apellido
        else: persona.apellido = apellido
            
        if hasattr(persona, 'Cedula'): persona.Cedula = cedula
        else: persona.cedula = cedula
            
        if hasattr(persona, 'Telefono'): persona.Telefono = telefono
        else: persona.telefono = telefono

        id_puesto = request.form.get('idPuestoTrabajo')
        if hasattr(trabajador_obj, 'IdPuestoTrabajo'):
            trabajador_obj.IdPuestoTrabajo = int(id_puesto) if id_puesto else None
        else:
            trabajador_obj.idPuestoTrabajo = int(id_puesto) if id_puesto else None

        sueldo_raw = request.form.get('sueldo')
        sueldo_val = sueldo_raw.replace(',', '.') if sueldo_raw else '0'
        if hasattr(trabajador_obj, 'Sueldo'):
            trabajador_obj.Sueldo = sueldo_val
        else:
            trabajador_obj.sueldo = sueldo_val
        
        db.session.commit()
        flash('Datos del trabajador modificados exitosamente', 'success')
        return redirect(url_for('trabajador.query_workers'))
        
    return render_template('modificar_trabajador.html', trabajador=trabajador_obj, puestos=puestos)

@workers_blueprint.route('/trabajador/eliminar/<int:id>', methods=['POST'])
def delete_worker(id):
    trabajador_obj = Trabajador.query.get_or_404(id)
    persona = getattr(trabajador_obj, 'Persona', getattr(trabajador_obj, 'persona', None))
    
    # Eliminación física en PostgreSQL
    db.session.delete(trabajador_obj)
    if persona:
        db.session.delete(persona)
        
    db.session.commit()
    
    flash('Trabajador eliminado exitosamente', 'success')
    return redirect(url_for('trabajador.query_workers'))

@workers_blueprint.route('/trabajador/reporte', methods=['GET'])
def generate_report():
    idPuestoTrabajo = request.args.get('idPuestoTrabajo')
    
    if idPuestoTrabajo:
        trabajadores = Trabajador.query.filter_by(idPuestoTrabajo=idPuestoTrabajo).all()
    else:
        trabajadores = Trabajador.query.all()

    puestos = PuestoTrabajo.query.all()    
    return render_template('pdf_workers.html', trabajadores=trabajadores, puestos=puestos)