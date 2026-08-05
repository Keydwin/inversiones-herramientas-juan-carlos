from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# We initialize SQLAlchemy (we will connect it to Flask later).
db = SQLAlchemy()

class Usuario(db.Model): 
    __tablename__ = 'usuario'
    
    IdUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdTrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.IdTrabajador'), nullable=False)
    NombreUsuario = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Method for securely creating the password (do not store in plain text)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    # Method to verify if the password is correct
    def check_password(self, password): 
        return check_password_hash(self.password, password)