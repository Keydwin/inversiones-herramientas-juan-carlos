import io, os
from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response, current_app
from models import db, Usuario, Trabajador
from sqlalchemy.exc import IntegrityError
from xhtml2pdf import pisa

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/usuarios')
def query_users():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('user', '', type=str).strip()
    
    per_page = 11

    query = Usuario.query.join(Usuario.trabajador).order_by(Usuario.IdUsuario.asc())

    if search_query:
        query = query.filter(Usuario.NombreUsuario.ilike(f"%{search_query}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Obtener IDs de trabajadores que ya tienen usuario
    trabajadores_ocupados_ids = [u.IdTrabajador for u in Usuario.query.with_entities(Usuario.IdTrabajador).all()]
    
    # Filtrar solo los trabajadores disponibles
    trabajadores_disponibles = Trabajador.query.filter(
        ~Trabajador.IdTrabajador.in_(trabajadores_ocupados_ids)
    ).all() if trabajadores_ocupados_ids else Trabajador.query.all()

    trabajadores = Trabajador.query.all()

    return render_template(
        'user.html', 
        pagination=pagination, 
        search_query=search_query, 
        trabajadores=trabajadores,
        trabajadores_disponibles=trabajadores_disponibles,
        trabajadores_ocupados_ids=trabajadores_ocupados_ids
    )

@user_blueprint.route('/usuarios/register_user', methods=['POST'])
def register_user():
    username = request.form.get('NombreUsuario', '').strip()
    id_trabajador = request.form.get('IdTrabajador')
    password = request.form.get('password', '').strip()

    existe_usuario = Usuario.query.filter_by(NombreUsuario=username).first()
    if existe_usuario:
        flash("El nombre de usuario ya se encuentra registrado", "danger")
        return redirect(url_for('user.query_users'))

    existe_trabajador = Usuario.query.filter_by(IdTrabajador=id_trabajador).first()
    if existe_trabajador:
        flash("El trabajador seleccionado ya tiene un usuario asignado", "danger")
        return redirect(url_for('user.query_users'))

    if username and id_trabajador and password:
        # Se guarda la contraseña tal cual en texto plano
        new_user = Usuario(
            NombreUsuario=username,
            IdTrabajador=id_trabajador,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito.', 'success')

    return redirect(url_for('user.query_users'))

@user_blueprint.route('/usuarios/update_user/<int:IdUsuario>', methods=['POST'])
def update_user(IdUsuario):
    user = Usuario.query.get_or_404(IdUsuario)
    username = request.form.get('NombreUsuario', '').strip()
    id_trabajador = request.form.get('IdTrabajador')
    password = request.form.get('password', '').strip()

    if username:
        user.NombreUsuario = username
    if id_trabajador:
        user.IdTrabajador = id_trabajador
    if password:
        user.password = password

    db.session.commit()
    flash('Usuario modificado con éxito.', 'success')

    return redirect(url_for('user.query_users'))

@user_blueprint.route('/usuarios/delete_user/<int:IdUsuario>', methods=['POST'])
def delete_user(IdUsuario):
    try:
        user = Usuario.query.get_or_404(IdUsuario)
        db.session.delete(user)
        db.session.commit()
        flash('Usuario eliminado exitosamente', 'success')
        
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar el usuario porque tiene registros asociados', 'danger')
        
    except Exception:
        db.session.rollback()
        flash('Error al intentar eliminar el usuario', 'danger')
    
    return redirect(url_for('user.query_users'))

@user_blueprint.route('/usuarios/user_report')
def generate_user_report():
    users = Usuario.query.order_by(Usuario.NombreUsuario).all()
    ruta_static = os.path.join(current_app.root_path, 'static')
    
    html_renderizado = render_template('pdf_user.html', users=users, base_dir=ruta_static)
    output_memoria = io.BytesIO()
    
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)
    
    if pisa_status.err:
        return "Error al generar el PDF", 500
        
    output_memoria.seek(0)
    
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_usuarios.pdf'
    
    return response