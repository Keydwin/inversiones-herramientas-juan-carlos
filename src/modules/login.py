from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from models import Usuario

login_blueprint = Blueprint('login', __name__)

def _obtener_credenciales():
    """Get credentials from JSON or HTML form."""
    if request.is_json:
        data = request.get_json(silent=True) or {}
        username = (data.get('usuario') or data.get('NombreUsuario') or '').strip()
        password = (data.get('password') or data.get('contraseña') or '').strip()
        return username, password

    username = (request.form.get('usuario') or request.form.get('NombreUsuario') or '').strip()
    password = (request.form.get('password') or request.form.get('contraseña') or '').strip()
    return username, password


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Render login page and authenticate user."""
    if session.get('usuario_id') and request.method == 'GET':
        return redirect(url_for('product.query_products'))

    if request.method == 'GET':
        return render_template('login.html')

    username, password = _obtener_credenciales()

    if not username or not password:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Debe llenar todos los campos.'}), 400
        return render_template('login.html')

    usuario_db = Usuario.query.filter_by(NombreUsuario=username).first()

    # Comparación directa de texto plano sin encriptación
    if usuario_db and usuario_db.password.strip() == password:
        session.clear()
        session['usuario_id'] = usuario_db.IdUsuario
        session['usuario'] = usuario_db.NombreUsuario.strip() if usuario_db.NombreUsuario else usuario_db.NombreUsuario

        if request.is_json:
            return jsonify({'success': True, 'redirect': url_for('product.query_products')})

        return redirect(url_for('product.query_products'))

    if request.is_json:
        return jsonify({'success': False, 'error': 'Usuario o contraseña incorrectos.'}), 401

    return render_template('login.html')


@login_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    """Clear user session and redirect to login."""
    session.clear()
    return redirect(url_for('login.login'))


@login_blueprint.before_app_request
def requerir_login():
    """Protect routes silently without flash messages."""
    public_endpoints = ['login.login', 'static']

    if request.endpoint and request.endpoint not in public_endpoints:
        if not session.get('usuario_id'):
            if request.is_json:
                return jsonify({'success': False}), 401
            return redirect(url_for('login.login'))