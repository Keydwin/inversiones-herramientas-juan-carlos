from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Creating classes for PostgreSQL tables

class Cliente(db.Model):
    __tablename__ = 'cliente'
    IdCliente = db.Column(db.Integer, primary_key=True)
    IdPersona = db.Column(db.Integer, db.ForeignKey('persona.IdPersona'), nullable=False)
    IdParroquia = db.Column(db.Integer, db.ForeignKey('parroquia.IdParroquia'), nullable=False)
    Direccion = db.Column(db.String(255), nullable=False)

    persona = db.relationship('Persona', backref=db.backref('cliente', uselist=False))
    parroquia = db.relationship('Parroquia', backref=db.backref('clientes', lazy=True))

class Compra(db.Model):
    __tablename__ = 'compra'
    IdCompra = db.Column(db.Integer, primary_key=True)
    IdProducto = db.Column(db.Integer, db.ForeignKey('producto.IdProducto'), nullable=False)
    Fecha = db.Column(db.Date, nullable=False)
    MontoTotal = db.Column(db.Numeric(10, 2), nullable=False)

    producto = db.relationship('Producto', backref=db.backref('compras', lazy=True))

class Estado(db.Model):
    __tablename__ = 'estado'
    IdEstado = db.Column(db.Integer, primary_key=True)
    Estado = db.Column(db.String(255), nullable=False)

class Inventario(db.Model):
    __tablename__ = 'inventario'
    IdInventario = db.Column(db.Integer, primary_key=True)
    IdProducto = db.Column(db.Integer, db.ForeignKey('producto.IdProducto'), nullable=False)
    CantidadProducto = db.Column(db.Integer, nullable=False)

    producto = db.relationship('Producto', backref=db.backref('inventario', uselist=False))

class Marca(db.Model):
    __tablename__ = 'marca'
    IdMarca = db.Column(db.Integer, primary_key=True)
    Marca = db.Column(db.String(255), nullable=False)

class Municipio(db.Model):
    __tablename__ = 'municipio'
    IdMunicipio = db.Column(db.Integer, primary_key=True)
    IdEstado = db.Column(db.Integer, db.ForeignKey('estado.IdEstado'), nullable=False)
    Municipio = db.Column(db.String(255), nullable=False)

    estado = db.relationship('Estado', backref=db.backref('municipios', lazy=True))

class Parroquia(db.Model):
    __tablename__ = 'parroquia'
    IdParroquia = db.Column(db.Integer, primary_key=True)
    IdMunicipio = db.Column(db.Integer, db.ForeignKey('municipio.IdMunicipio'), nullable=False)
    Parroquia = db.Column(db.String(255), nullable=False)

    municipio = db.relationship('Municipio', backref=db.backref('parroquias', lazy=True))

class Persona(db.Model):
    __tablename__ = 'persona'
    IdPersona = db.Column(db.Integer, primary_key=True)
    Cedula = db.Column(db.Integer, nullable=False)
    Nombre = db.Column(db.String(255), nullable=False)
    Apellido = db.Column(db.String(255), nullable=False)
    Telefono = db.Column(db.Integer, nullable=False)

class Producto(db.Model):
    __tablename__ = 'producto'
    IdProducto = db.Column(db.Integer, primary_key=True)
    IdMarca = db.Column(db.Integer, db.ForeignKey('marca.IdMarca'), nullable=False)
    Codigo = db.Column(db.Integer, nullable=False)
    NombreProducto = db.Column(db.String(255), nullable=False)
    Descripcion = db.Column(db.String(255), nullable=False)
    PrecioDeContado = db.Column(db.Numeric(10, 2), nullable=False)
    PrecioCredito = db.Column(db.Numeric(10, 2), nullable=False)

    marca = db.relationship('Marca', backref=db.backref('productos', lazy=True))

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    IdProveedor = db.Column(db.Integer, primary_key=True)
    NombreProveedor = db.Column(db.String(255), nullable=False)

class PuestoTrabajo(db.Model):
    __tablename__ = 'puestotrabajo'
    IdPuestoTrabajo = db.Column(db.Integer, primary_key=True)
    NombrePuestoTrabajo = db.Column(db.String(255), nullable=False)
    Sueldo = db.Column(db.Numeric(10, 2), nullable=False)

class Trabajador(db.Model):
    __tablename__ = 'trabajador'
    IdTrabajador = db.Column(db.Integer, primary_key=True)
    IdPersona = db.Column(db.Integer, db.ForeignKey('persona.IdPersona'), nullable=False)
    IdPuestoTrabajo = db.Column(db.Integer, db.ForeignKey('puestotrabajo.IdPuestoTrabajo'), nullable=False)

    persona = db.relationship('Persona', backref=db.backref('trabajador', uselist=False))
    puesto = db.relationship('PuestoTrabajo', backref=db.backref('trabajadores', lazy=True))

class Usuario(db.Model):
    __tablename__ = 'usuario'
    IdUsuario = db.Column(db.Integer, primary_key=True)
    IdTrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.IdTrabajador'), nullable=False)
    NombreUsuario = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    trabajador = db.relationship('Trabajador', backref=db.backref('usuario', uselist=False))

class Venta(db.Model):
    __tablename__ = 'venta'
    IdVenta = db.Column(db.Integer, primary_key=True)
    IdTrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.IdTrabajador'), nullable=False)
    IdCliente = db.Column(db.Integer, db.ForeignKey('cliente.IdCliente'), nullable=False)
    IdInventario = db.Column(db.Integer, db.ForeignKey('inventario.IdInventario'), nullable=False)
    FechaVenta = db.Column(db.Date, nullable=False)
    MetodoPago = db.Column(db.String(255), nullable=False)
    MontoTotal = db.Column(db.Numeric(10, 2), nullable=False)

    trabajador = db.relationship('Trabajador', backref=db.backref('ventas', lazy=True))
    cliente = db.relationship('Cliente', backref=db.backref('ventas', lazy=True))
    inventario = db.relationship('Inventario', backref=db.backref('ventas', lazy=True))

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    estatus = db.Column(db.String(20), default='activo', nullable=False)

class Venta(db.Model):
    __tablename__ = 'ventas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now, nullable=False)
    metodo_pago = db.Column(db.String(20), nullable=False)
    monto_total = db.Column(db.Numeric(12, 2), default=0.00, nullable=False)
    estado_entrega = db.Column(db.String(20), default='Pendiente', nullable=False)

    cliente = db.relationship('Cliente', backref='ventas')
    vendedor = db.relationship('Usuario', backref='ventas_realizadas')
    detalles = db.relationship('DetalleVenta', backref='venta', cascade='all, delete-orphan')


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'

    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    producto = db.relationship('Producto')

class Puesto(db.Model):
    __tablename__ = 'puesto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Trabajador(db.Model):
    __tablename__ = 'trabajador'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(120))
    estatus = db.Column(db.String(20), default='activo')
    puesto_id = db.Column(db.Integer, db.ForeignKey('puesto.id'), nullable=False)

class PuestoTrabajo(db.Model):
    __tablename__ = 'puesto_trabajo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    obligaciones = db.Column(db.Text, nullable=False)
    sueldo = db.Column(db.Numeric(10, 2), nullable=False)

    def __init__(self, nombre, obligaciones, sueldo):
        self.nombre = nombre
        self.obligaciones = obligaciones
        self.sueldo = sueldo













