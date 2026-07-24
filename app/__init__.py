"""
Sistema de Gestión de Talleres de Impresoras
Arquitectura Mobile First - 100% Offline
"""

import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

# Inicialización de extensiones
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_object=None):
    """Factory pattern para crear la aplicación Flask"""
    
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuración por defecto
    app.config['SECRET_KEY'] = 'tu-clave-secreta-muy-segura-cambiar-en-produccion'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////workspace/instance/taller_impresoras.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'timeout': 30}
    }
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
    
    if config_object:
        app.config.from_object(config_object)
    
    # Asegurar directorio instance
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configurar Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Registrar Blueprints
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from .dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    from .clientes import bp as clientes_bp
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    
    from .equipos import bp as equipos_bp
    app.register_blueprint(equipos_bp, url_prefix='/equipos')
    
    from .ordenes import bp as ordenes_bp
    app.register_blueprint(ordenes_bp, url_prefix='/ordenes')
    
    from .tecnicos import bp as tecnicos_bp
    app.register_blueprint(tecnicos_bp, url_prefix='/tecnicos')
    
    from .inventario import bp as inventario_bp
    app.register_blueprint(inventario_bp, url_prefix='/inventario')
    
    from .proveedores import bp as proveedores_bp
    app.register_blueprint(proveedores_bp, url_prefix='/proveedores')
    
    from .usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    
    from .reportes import bp as reportes_bp
    app.register_blueprint(reportes_bp, url_prefix='/reportes')
    
    from .configuracion import bp as configuracion_bp
    app.register_blueprint(configuracion_bp, url_prefix='/configuracion')
    
    from .backup import bp as backup_bp
    app.register_blueprint(backup_bp, url_prefix='/backup')
    
    # Crear tablas de base de datos
    with app.app_context():
        db.create_all()
        # Crear usuario administrador por defecto si no existe
        from .models import Usuario
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            admin = Usuario(
                username='admin',
                email='admin@taller.com',
                password_hash=generate_password_hash('admin123'),
                nombre='Administrador',
                rol='administrador',
                activo=True
            )
            db.session.add(admin)
            db.session.commit()
    
    @app.route('/')
    def index():
        if login_manager.current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    return app
