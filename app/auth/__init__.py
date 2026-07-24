"""
Blueprint de Autenticación
Login, Logout, Recuperación, Cambio de contraseña
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from .. import db
from ..models import Usuario, ActividadUsuario

bp = Blueprint('auth', __name__, template_folder='../../templates/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and usuario.check_password(password) and usuario.activo:
            login_user(usuario, remember=remember)
            usuario.ultimo_acceso = db.func.now()
            db.session.commit()
            
            # Registrar actividad
            actividad = ActividadUsuario(
                usuario_id=usuario.id,
                accion='LOGIN',
                descripcion=f'Inicio de sesión exitoso',
                ip_address=request.remote_addr
            )
            db.session.add(actividad)
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Usuario o contraseña inválidos', 'danger')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    # Registrar actividad
    actividad = ActividadUsuario(
        usuario_id=current_user.id,
        accion='LOGOUT',
        descripcion=f'Cierre de sesión',
        ip_address=request.remote_addr
    )
    db.session.add(actividad)
    db.session.commit()
    
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    # En producción implementar envío de email o preguntas de seguridad
    if request.method == 'POST':
        email = request.form.get('email')
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario:
            flash('Se ha enviado un enlace de recuperación a su correo', 'info')
        else:
            flash('No se encontró una cuenta con ese correo', 'warning')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/recuperar.html')

@bp.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    if request.method == 'POST':
        password_actual = request.form.get('password_actual')
        password_nuevo = request.form.get('password_nuevo')
        password_confirm = request.form.get('password_confirm')
        
        if not current_user.check_password(password_actual):
            flash('La contraseña actual es incorrecta', 'danger')
            return render_template('auth/cambiar_password.html')
        
        if password_nuevo != password_confirm:
            flash('Las nuevas contraseñas no coinciden', 'danger')
            return render_template('auth/cambiar_password.html')
        
        if len(password_nuevo) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'warning')
            return render_template('auth/cambiar_password.html')
        
        current_user.set_password(password_nuevo)
        db.session.commit()
        
        # Registrar actividad
        actividad = ActividadUsuario(
            usuario_id=current_user.id,
            accion='CAMBIO_PASSWORD',
            descripcion='Cambio de contraseña',
            ip_address=request.remote_addr
        )
        db.session.add(actividad)
        db.session.commit()
        
        flash('Contraseña cambiada exitosamente', 'success')
        return redirect(url_for('dashboard.index'))
    
    return render_template('auth/cambiar_password.html')
