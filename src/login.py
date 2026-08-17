from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from models import Usuario

# We created the blueprint to handle all authentication routes.
login_blueprint = Blueprint('login', __name__)
def _obtener_credenciales():
    """Obtiene las credenciales desde JSON o desde el formulario HTML."""
    if request.is_json:
        datos = request.get_json(silent=True) or {}
        usuario = (datos.get('usuario') or '').strip()
        password = (datos.get('password') or datos.get('contraseña') or '').strip()
        return usuario, password

    usuario = (request.form.get('usuario') or '').strip()
    password = (request.form.get('password') or request.form.get('contraseña') or '').strip()
    return usuario, password


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Muestra la vista de inicio de sesión y valida al usuario."""
    # If there is already an active session, it does not allow returning to the login
    if session.get('usuario_id') and request.method == 'GET':
        return redirect(url_for('product.query_products'))

    if request.method == 'GET':
        return render_template('login.html')

    usuario, password = _obtener_credenciales()

    # Basic validation of empty fields
    if not usuario or not password:
        if request.is_json:
            return jsonify({
                'success': False,
                'error': 'Debe llenar todos los campos.'
            }), 400

        flash('Debe llenar todos los campos.', 'danger')
        return render_template('login.html')

    # We search for the user in the usuario table using the NombreUsuario field
    usuario_db = Usuario.query.filter_by(NombreUsuario=usuario).first()

    # Validation of user and password
    if usuario_db and usuario_db.password == password:
        session.clear()
        session['usuario_id'] = usuario_db.IdUsuario
        session['usuario'] = usuario_db.NombreUsuario

        if request.is_json:
            return jsonify({
                'success': True,
                'redirect': url_for('product.query_products')
            })

        flash('Inicio de sesión correcto.', 'success')
        return redirect(url_for('product.query_products'))

    if request.is_json:
        return jsonify({
            'success': False,
            'error': 'Usuario o contraseña incorrectos.'
        }), 401

    flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

# The logout is recorded here.
@login_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    """Cierra la sesión del usuario y lo devuelve al login."""
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('login.login'))
