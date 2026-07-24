"""
Modelos de la base de datos
Sistema normalizado con relaciones mediante claves foráneas
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

# Tablas intermedias para relaciones muchos a muchos
orden_tecnico = db.Table('orden_tecnico',
    db.Column('orden_id', db.Integer, db.ForeignKey('ordenes.id'), primary_key=True),
    db.Column('tecnico_id', db.Integer, db.ForeignKey('tecnicos.id'), primary_key=True)
)

class Usuario(UserMixin, db.Model):
    """Modelo de usuarios del sistema"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='consulta')  # administrador, recepcionista, tecnico, consulta
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime)
    
    # Relaciones
    actividades = db.relationship('ActividadUsuario', backref='usuario', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.username}>'


class ActividadUsuario(db.Model):
    """Registro de actividad de usuarios"""
    __tablename__ = 'actividades_usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    accion = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)


class Cliente(db.Model):
    """Modelo de clientes"""
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, index=True)
    tipo_documento = db.Column(db.String(20), default='DNI')  # DNI, RUC, CE, PASAPORTE
    numero_documento = db.Column(db.String(20), unique=True, nullable=False, index=True)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(100))
    observaciones = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    equipos = db.relationship('Equipo', backref='cliente', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cliente {self.nombre}>'


class Equipo(db.Model):
    """Modelo de equipos/impresoras"""
    __tablename__ = 'equipos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    marca = db.Column(db.String(100), nullable=False, index=True)
    modelo = db.Column(db.String(100), nullable=False)
    numero_serie = db.Column(db.String(50), index=True)
    tipo_equipo = db.Column(db.String(50))  # Impresora láser, Inkjet, Multifuncional, Plotter, etc.
    accesorios = db.Column(db.Text)  # Lista de accesorios separados por coma
    estado_fisico = db.Column(db.Text)  # Descripción del estado físico
    observaciones = db.Column(db.Text)
    foto_path = db.Column(db.String(255))  # Ruta de la foto del equipo
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    ordenes = db.relationship('Orden', backref='equipo', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Equipo {self.marca} {self.modelo}>'


class Orden(db.Model):
    """Modelo de órdenes de trabajo"""
    __tablename__ = 'ordenes'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_orden = db.Column(db.String(20), unique=True, nullable=False, index=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_diagnostico = db.Column(db.DateTime)
    fecha_presupuesto = db.Column(db.DateTime)
    fecha_reparacion = db.Column(db.DateTime)
    fecha_entrega = db.Column(db.DateTime)
    
    # Estados: recibido, diagnostico, presupuesto, autorizada, reparacion, listo, entregada, cancelada
    estado = db.Column(db.String(30), default='recibido', index=True)
    
    # Datos de recepción
    motivo_ingreso = db.Column(db.Text, nullable=False)
    observaciones_recepcion = db.Column(db.Text)
    
    # Diagnóstico
    diagnostico = db.Column(db.Text)
    
    # Presupuesto
    presupuesto_mano_obra = db.Column(db.Float, default=0)
    presupuesto_repuestos = db.Column(db.Float, default=0)
    presupuesto_total = db.Column(db.Float, default=0)
    presupuesto_observaciones = db.Column(db.Text)
    presupuesto_aprobado = db.Column(db.Boolean, default=False)
    fecha_aprobacion = db.Column(db.DateTime)
    
    # Reparación
    trabajo_realizado = db.Column(db.Text)
    
    # Entrega
    observaciones_entrega = db.Column(db.Text)
    monto_cobrado = db.Column(db.Float, default=0)
    forma_pago = db.Column(db.String(50))  # Efectivo, Transferencia, Tarjeta, etc.
    
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    tecnicos = db.relationship('Tecnico', secondary=orden_tecnico, backref=db.backref('ordenes', lazy='dynamic'))
    movimientos = db.relationship('MovimientoInventario', backref='orden', lazy='dynamic')
    
    def __repr__(self):
        return f'<Orden {self.numero_orden}>'


class Tecnico(db.Model):
    """Modelo de técnicos"""
    __tablename__ = 'tecnicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, index=True)
    tipo_documento = db.Column(db.String(20), default='DNI')
    numero_documento = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    especialidad = db.Column(db.String(100))  # Especialidad técnica
    estado = db.Column(db.String(20), default='disponible')  # disponible, ocupado, inactivo
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tecnico {self.nombre}>'


class CategoriaInventario(db.Model):
    """Categorías de inventario"""
    __tablename__ = 'categorias_inventario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    productos = db.relationship('Producto', backref='categoria', lazy='dynamic')
    
    def __repr__(self):
        return f'<Categoria {self.nombre}>'


class Producto(db.Model):
    """Productos del inventario"""
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_inventario.id'), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(150), nullable=False, index=True)
    descripcion = db.Column(db.Text)
    marca = db.Column(db.String(100))
    precio_costo = db.Column(db.Float, default=0)
    precio_venta = db.Column(db.Float, default=0)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    unidad_medida = db.Column(db.String(20), default='UNIDAD')  # UNIDAD, JUEGO, KIT, etc.
    ubicacion = db.Column(db.String(50))  # Ubicación física en almacén
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    movimientos = db.relationship('MovimientoInventario', backref='producto', lazy='dynamic')
    
    def __repr__(self):
        return f'<Producto {self.codigo} - {self.nombre}>'


class MovimientoInventario(db.Model):
    """Movimientos de inventario (entradas/salidas)"""
    __tablename__ = 'movimientos_inventario'
    
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes.id'))
    tipo_movimiento = db.Column(db.String(20), nullable=False)  # entrada, salida
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    motivo = db.Column(db.Text)  # Motivo del movimiento
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    responsable = db.relationship('Usuario', backref='movimientos')
    
    def __repr__(self):
        return f'<Movimiento {self.tipo_movimiento} - {self.cantidad}>'


class Proveedor(db.Model):
    """Modelo de proveedores"""
    __tablename__ = 'proveedores'
    
    id = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(150), nullable=False, index=True)
    nombre_comercial = db.Column(db.String(100))
    tipo_documento = db.Column(db.String(20), default='RUC')
    numero_documento = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(100))
    pais = db.Column(db.String(50), default='Perú')
    contacto = db.Column(db.String(100))  # Persona de contacto
    telefono_contacto = db.Column(db.String(20))
    email_contacto = db.Column(db.String(120))
    observaciones = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    compras = db.relationship('Compra', backref='proveedor', lazy='dynamic')
    
    def __repr__(self):
        return f'<Proveedor {self.razon_social}>'


class Compra(db.Model):
    """Registro de compras a proveedores"""
    __tablename__ = 'compras'
    
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    numero_compra = db.Column(db.String(50), unique=True, nullable=False)
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    subtotal = db.Column(db.Float, default=0)
    igv = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    observaciones = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    detalles = db.relationship('CompraDetalle', backref='compra', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Compra {self.numero_compra}>'


class CompraDetalle(db.Model):
    """Detalles de compra"""
    __tablename__ = 'compras_detalles'
    
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    # Relaciones
    producto = db.relationship('Producto', backref='compras_detalles')
    
    def __repr__(self):
        return f'<CompraDetalle {self.cantidad} x {self.producto.nombre}>'


class Configuracion(db.Model):
    """Configuración del sistema"""
    __tablename__ = 'configuracion'
    
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)
    descripcion = db.Column(db.String(200))
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Configuracion {self.clave}>'
