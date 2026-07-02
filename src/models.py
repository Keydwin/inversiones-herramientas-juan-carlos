from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Creating classes for PostgreSQL tables

class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    IdCliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdPersona = db.Column(db.Integer, db.ForeignKey('persona.IdPersona'), nullable=False)
    IdParroquia = db.Column(db.Integer, db.ForeignKey('parroquia.IdParroquia'), nullable=False)
    Direccion = db.Column(db.String(255), nullable=False)

    persona = db.relationship('Persona')
    parroquia = db.relationship('Parroquia')

class Compra(db.Model):
    __tablename__ = 'compra'
    
    IdCompra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdProveedor = db.Column(db.Integer, db.ForeignKey('proveedor.IdProveedor'), nullable=False)
    Fecha = db.Column(db.Date, nullable=False)
    MontoTotal = db.Column(db.Numeric(10, 2), nullable=False)

    proveedor = db.relationship('Proveedor')

class Estado(db.Model):
    __tablename__ = 'estado'
    
    IdEstado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Estado = db.Column(db.String(255), nullable=False)

class Inventario(db.Model):
    __tablename__ = 'inventario'
    
    IdInventario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdProducto = db.Column(db.Integer, db.ForeignKey('producto.IdProducto'), nullable=False)
    CantidadProducto = db.Column(db.Integer, nullable=False)

    producto = db.relationship('Producto')

class Marca(db.Model):
    __tablename__ = 'marca'
    
    IdMarca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Marca = db.Column(db.String(255), nullable=False)

class Municipio(db.Model):
    __tablename__ = 'municipio'
    
    IdMunicipio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdEstado = db.Column(db.Integer, db.ForeignKey('estado.IdEstado'), nullable=False)
    Municipio = db.Column(db.String(255), nullable=False)

    estado = db.relationship('Estado')

class Parroquia(db.Model):
    __tablename__ = 'parroquia'
    
    IdParroquia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdMunicipio = db.Column(db.Integer, db.ForeignKey('municipio.IdMunicipio'), nullable=False)
    Parroquia = db.Column(db.String(255), nullable=False)

    municipio = db.relationship('Municipio')

class Persona(db.Model):
    __tablename__ = 'persona'
    
    IdPersona = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cedula = db.Column(db.Integer, nullable=False)
    Nombre = db.Column(db.String(255), nullable=False)
    Apellido = db.Column(db.String(255), nullable=False)
    Telefono = db.Column(db.Integer, nullable=False)

class Producto(db.Model):
    __tablename__ = 'producto'
    
    IdProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdMarca = db.Column(db.Integer, db.ForeignKey('marca.IdMarca'), nullable=False)
    Codigo = db.Column(db.Integer, nullable=False)
    NombreProducto = db.Column(db.String(255), nullable=False)
    Descripcion = db.Column(db.String(255), nullable=False)
    PrecioDeContado = db.Column(db.Numeric(10, 2), nullable=False)
    PrecioCredito = db.Column(db.Numeric(10, 2), nullable=False)

    marca = db.relationship('Marca')

class ProductoCompra(db.Model):
    __tablename__ = 'productocompra'
    
    IdProductoCompra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdProducto = db.Column(db.Integer, db.ForeignKey('producto.IdProducto'), nullable=False)
    IdCompra = db.Column(db.Integer, db.ForeignKey('compra.IdCompra'), nullable=False)
    Cantidad = db.Column(db.Integer, nullable=False)
    PrecioDecontado = db.Column(db.Numeric(10, 2), nullable=False)
    PrecioCredito = db.Column(db.Numeric(10, 2), nullable=False)

    producto = db.relationship('Producto')
    compra = db.relationship('Compra')

class ProductoVenta(db.Model):
    __tablename__ = 'productoventa'
    
    IdProductoVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdVenta = db.Column(db.Integer, db.ForeignKey('venta.IdVenta'), nullable=False)
    IdProducto = db.Column(db.Integer, db.ForeignKey('producto.IdProducto'), nullable=False)
    Cantidad = db.Column(db.Integer, nullable=False)

    venta = db.relationship('Venta')
    producto = db.relationship('Producto')

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    
    IdProveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NombreProveedor = db.Column(db.String(255), nullable=False)

class PuestoTrabajo(db.Model):
    __tablename__ = 'puestotrabajo'
    
    IdPuestoTrabajo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NombrePuestoTrabajo = db.Column(db.String(255), nullable=False)
    Sueldo = db.Column(db.Numeric(10, 2), nullable=False)

class Trabajador(db.Model):
    __tablename__ = 'trabajador'
    
    IdTrabajador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdPersona = db.Column(db.Integer, db.ForeignKey('persona.IdPersona'), nullable=False)
    IdPuestoTrabajo = db.Column(db.Integer, db.ForeignKey('puestotrabajo.IdPuestoTrabajo'), nullable=False)

    persona = db.relationship('Persona')
    puesto_trabajo = db.relationship('PuestoTrabajo')

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    IdUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdTrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.IdTrabajador'), nullable=False)
    NombreUsuario = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    trabajador = db.relationship('Trabajador')

class Venta(db.Model):
    __tablename__ = 'venta'
    
    IdVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdTrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.IdTrabajador'), nullable=False)
    IdCliente = db.Column(db.Integer, db.ForeignKey('cliente.IdCliente'), nullable=False)
    FechaVenta = db.Column(db.Date, nullable=False)
    MetodoPago = db.Column(db.String(255), nullable=False)
    MontoTotal = db.Column(db.Numeric(10, 2), nullable=False)

    trabajador = db.relationship('Trabajador')
    cliente = db.relationship('Cliente')












