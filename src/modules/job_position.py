import io, os
from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response, current_app
from models import db, PuestoTrabajo  
from sqlalchemy.exc import IntegrityError
from xhtml2pdf import pisa

# Create the Blueprint for the job position module
job_position_blueprint = Blueprint('job_position', __name__)

@job_position_blueprint.route('/puestos_trabajo')
def query_job_positions():
    # Get URL parameters
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('job_position', '', type=str).strip()
    
    per_page = 11  # Rows per page

    # Query and sort from the PuestoTrabajo model
    query = PuestoTrabajo.query.order_by(PuestoTrabajo.IdPuestoTrabajo.asc())

    # Apply search filter if query exists
    if search_query:
        query = query.filter(PuestoTrabajo.NombrePuestoTrabajo.ilike(f"%{search_query}%"))

    # Execute pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Render template with data
    return render_template('job_position.html', pagination=pagination, search_query=search_query)

@job_position_blueprint.route('/puestos_trabajo/register_job_position', methods=['POST'])
def register_job_position():
    # Get values from form input
    position_name = request.form.get('NombrePuestoTrabajo', '').strip()
    salary = request.form.get('Sueldo', '').strip()
        
    # Verify that no job position with the same name exists
    existe = PuestoTrabajo.query.filter(PuestoTrabajo.NombrePuestoTrabajo.ilike(position_name)).first()
    if existe:
        flash("Este puesto de trabajo ya se encuentra registrado", "danger")
        return redirect(url_for('job_position.query_job_positions'))

    # Clean and save to database if valid
    if position_name and salary:
        try:
            new_position = PuestoTrabajo(
                NombrePuestoTrabajo=position_name,
                Sueldo=float(salary)
            )
            db.session.add(new_position)
            db.session.commit()
            flash('Puesto de trabajo registrado con éxito.', 'success')
        except Exception:
            db.session.rollback()
            flash('Error al intentar registrar el puesto de trabajo.', 'danger')
            
    # Redirect back to job positions list
    return redirect(url_for('job_position.query_job_positions'))

@job_position_blueprint.route('/puestos_trabajo/update_job_position/<int:IdPuestoTrabajo>', methods=['POST'])
def update_job_position(IdPuestoTrabajo):
    # Search in database using the exact ID
    position = PuestoTrabajo.query.get_or_404(IdPuestoTrabajo)
    position_name = request.form.get('NombrePuestoTrabajo', '').strip()
    salary = request.form.get('Sueldo', '').strip()
    
    if position_name and salary:
        try:
            position.NombrePuestoTrabajo = position_name
            position.Sueldo = float(salary)
            db.session.commit()
            flash('Puesto de trabajo modificado con éxito.', 'success')
        except Exception:
            db.session.rollback()
            flash('Error al intentar modificar el puesto de trabajo.', 'danger')
        
    return redirect(url_for('job_position.query_job_positions'))

@job_position_blueprint.route('/puestos_trabajo/delete_job_position/<int:IdPuestoTrabajo>', methods=['POST'])
def delete_job_position(IdPuestoTrabajo):
    try:
        # Consult job position model
        position = PuestoTrabajo.query.get_or_404(IdPuestoTrabajo)
        db.session.delete(position)
        db.session.commit()
        flash('Puesto de trabajo eliminado exitosamente.', 'success')
        
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar el puesto de trabajo porque tiene trabajadores asociados.', 'danger')
        
    except Exception:
        db.session.rollback()
        flash('Error al intentar eliminar el puesto de trabajo.', 'danger')
    
    return redirect(url_for('job_position.query_job_positions'))

@job_position_blueprint.route('/puestos_trabajo/job_position_report')
def generate_job_position_report():
    # Get data from PostgreSQL
    positions = PuestoTrabajo.query.order_by(PuestoTrabajo.NombrePuestoTrabajo).all()
    
    # Absolute path to static folder
    ruta_static = os.path.join(current_app.root_path, 'static')
    
    # Render HTML template with data and static path
    html_renderizado = render_template('pdf_job_position.html', positions=positions, base_dir=ruta_static)
    
    # Create an in-memory byte buffer
    output_memoria = io.BytesIO()
    
    # Convert HTML to PDF and store it in memory
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)
    
    # Check for rendering errors
    if pisa_status.err:
        return "Error al generar el PDF", 500
        
    # Move pointer to the beginning of the buffer
    output_memoria.seek(0)
    
    # Send PDF file back to browser as a download
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_puestos_trabajo.pdf'
    
    return response