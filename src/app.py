from flask import Flask, render_template, redirect, request, url_for, session, jsonify
import os
from models import db, Usuario

app = Flask(__name__)

# Configuring the PostgreSQL connection
app.secret_key = os.environ.get('SECRET_KEY', 'mi_clave_super_secreta_123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/SISGE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --Routes--

@app.route('/')
def index():
    return render_template('login.html')
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre_usuario = data.get('usuario') or data.get('NombreUsuario')
    contraseña = data.get('contraseña') or data.get('password')

    if not nombre_usuario or not contraseña:
        return jsonify({'success': False, 'error': 'Debe enviar usuario y contraseña'}), 400

    # We searched for the user in the database using SQLAlchemy
    user = Usuario.query.filter_by(NombreUsuario=nombre_usuario).first()

    # We verify whether it exists and if the password is correct.
    if user and user.check_password(contraseña):
        session['id_usuario'] = user.IdUsuario
        session['nombre_usuario'] = user.NombreUsuario
        session['id_trabajador'] = user.IdTrabajador
        return jsonify({'success': True, 'mensaje': 'Login exitoso'})
    else:
        return jsonify({'success': False, 'error': 'Usuario o contraseña incorrectos'}), 401

@app.route('/dashboard')
def dashboard():
    if 'nombre_usuario' not in session:
        return redirect(url_for('index'))
    return jsonify({'success': True, 'mensaje': f'Bienvenido {session["nombre_usuario"]}'})


if __name__ == '__main__':
    app.run(debug=True)
