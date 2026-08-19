import io, os
from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response, current_app
from models import db, Trabajador, Persona, PuestoTrabajo
from sqlalchemy.exc import IntegrityError
from xhtml2pdf import pisa

# Create the Blueprint for the worker module
worker_blueprint = Blueprint('worker', __name__)

@worker_blueprint.route('/trabajadores')
def query_workers():
    # Get URL query parameters for pagination and search
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('worker', '', type=str).strip()
    
    per_page = 11  # Rows per page

    # Query workers joining Persona and PuestoTrabajo
    query = Trabajador.query.join(Persona).join(PuestoTrabajo).order_by(Trabajador.IdTrabajador.asc())

    # Apply search filter by Cédula, Name or Last Name
    if search_query:
        query = query.filter(
            (Persona.Cedula.cast(db.String).ilike(f"%{search_query}%")) |
            (Persona.Nombre.ilike(f"%{search_query}%")) |
            (Persona.Apellido.ilike(f"%{search_query}%"))
        )

    # Execute pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Get all active job positions for selection forms
    positions = PuestoTrabajo.query.order_by(PuestoTrabajo.NombrePuestoTrabajo.asc()).all()

    # Render template with dataset
    return render_template('worker.html', pagination=pagination, search_query=search_query, positions=positions)

@worker_blueprint.route('/trabajadores/register_worker', methods=['POST'])
def register_worker():
    # Get values from form input
    cedula = request.form.get('Cedula', '').strip()
    nombre = request.form.get('Nombre', '').strip()
    apellido = request.form.get('Apellido', '').strip()
    telefono = request.form.get('Telefono', '').strip()
    id_puesto = request.form.get('IdPuestoTrabajo', '').strip()

    if cedula and nombre and apellido and telefono and id_puesto:
        try:
            # Check if Persona already exists
            persona = Persona.query.filter_by(Cedula=int(cedula)).first()
            
            if persona:
                # Verify if this person is already registered as a worker
                worker_exists = Trabajador.query.filter_by(IdPersona=persona.IdPersona).first()
                if worker_exists:
                    flash('Esta cédula ya corresponde a un trabajador registrado.', 'danger')
                    return redirect(url_for('worker.query_workers'))
                
                # Update personal info if needed
                persona.Nombre = nombre
                persona.Apellido = apellido
                persona.Telefono = int(telefono)
            else:
                # Create a new Persona record
                persona = Persona(
                    Cedula=int(cedula),
                    Nombre=nombre,
                    Apellido=apellido,
                    Telefono=int(telefono)
                )
                db.session.add(persona)
                db.session.flush()  # Obtain assigned IdPersona

            # Create new Trabajador entry
            new_worker = Trabajador(
                IdPersona=persona.IdPersona,
                IdPuestoTrabajo=int(id_puesto)
            )
            db.session.add(new_worker)
            db.session.commit()
            flash('Trabajador registrado con éxito.', 'success')

        except ValueError:
            flash('La cédula y el teléfono deben ser números enteros válidos.', 'danger')
        except Exception:
            db.session.rollback()
            flash('Error al intentar registrar el trabajador.', 'danger')

    return redirect(url_for('worker.query_workers'))

@worker_blueprint.route('/trabajadores/update_worker/<int:IdTrabajador>', methods=['POST'])
def update_worker(IdTrabajador):
    # Fetch worker or return 404
    worker = Trabajador.query.get_or_404(IdTrabajador)
    
    cedula = request.form.get('Cedula', '').strip()
    nombre = request.form.get('Nombre', '').strip()
    apellido = request.form.get('Apellido', '').strip()
    telefono = request.form.get('Telefono', '').strip()
    id_puesto = request.form.get('IdPuestoTrabajo', '').strip()

    if cedula and nombre and apellido and telefono and id_puesto:
        try:
            # Verify if Cédula belongs to another Persona
            existing_persona = Persona.query.filter(Persona.Cedula == int(cedula), Persona.IdPersona != worker.IdPersona).first()
            if existing_persona:
                flash('La cédula ingresada pertenece a otra persona.', 'danger')
                return redirect(url_for('worker.query_workers'))

            # Update associated Persona data
            worker.persona.Cedula = int(cedula)
            worker.persona.Nombre = nombre
            worker.persona.Apellido = apellido
            worker.persona.Telefono = int(telefono)
            
            # Update job position reference
            worker.IdPuestoTrabajo = int(id_puesto)

            db.session.commit()
            flash('Trabajador modificado con éxito.', 'success')

        except ValueError:
            flash('Formato numérico inválido para Cédula o Teléfono.', 'danger')
        except Exception:
            db.session.rollback()
            flash('Error al intentar modificar los datos del trabajador.', 'danger')

    return redirect(url_for('worker.query_workers'))

@worker_blueprint.route('/trabajadores/delete_worker/<int:IdTrabajador>', methods=['POST'])
def delete_worker(IdTrabajador):
    try:
        # Locate worker and delete record
        worker = Trabajador.query.get_or_404(IdTrabajador)
        db.session.delete(worker)
        db.session.commit()
        flash('Trabajador eliminado exitosamente.', 'success')

    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar el trabajador porque posee registros asociados (ventas, usuarios, etc.).', 'danger')

    except Exception:
        db.session.rollback()
        flash('Error al intentar eliminar el trabajador.', 'danger')

    return redirect(url_for('worker.query_workers'))

@worker_blueprint.route('/trabajadores/worker_report')
def generate_worker_report():
    # Query all workers sorted by name
    workers = Trabajador.query.join(Persona).order_by(Persona.Nombre.asc()).all()
    
    # Path to static CSS folder
    ruta_static = os.path.join(current_app.root_path, 'static')
    
    # Render PDF template with dataset
    html_renderizado = render_template('pdf_worker.html', workers=workers, base_dir=ruta_static)
    
    # Create in-memory stream buffer
    output_memoria = io.BytesIO()
    
    # Convert HTML string into PDF output stream
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)
    
    if pisa_status.err:
        return "Error al generar el PDF", 500
        
    output_memoria.seek(0)
    
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_trabajadores.pdf'
    
    return response