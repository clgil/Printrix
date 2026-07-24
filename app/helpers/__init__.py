"""
Helpers y utilidades del sistema
Funciones reutilizables para toda la aplicación
"""

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def rol_required(roles):
    """Decorador para restringir acceso por roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.rol not in roles:
                flash('No tienes permisos para acceder a esta sección', 'warning')
                return redirect(url_for('dashboard.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def generar_numero_orden():
    """Genera un número de orden único"""
    from ..models import Orden
    from datetime import datetime
    
    ano = datetime.now().year
    ultimo = Orden.query.order_by(Orden.id.desc()).first()
    
    if ultimo:
        numero = ultimo.id + 1
    else:
        numero = 1
    
    return f"OT-{ano}-{numero:06d}"

def formato_moneda(cantidad, moneda='S/.'):
    """Formatea una cantidad como moneda"""
    return f"{moneda} {cantidad:,.2f}"

def estado_color(estado):
    """Retorna el color Bootstrap según el estado"""
    colores = {
        'recibido': 'info',
        'diagnostico': 'warning',
        'presupuesto': 'warning',
        'autorizada': 'primary',
        'reparacion': 'primary',
        'esperando_piezas': 'secondary',
        'listo': 'success',
        'entregada': 'success',
        'cancelada': 'danger'
    }
    return colores.get(estado, 'secondary')

def estado_badge(estado):
    """Retorna el badge HTML según el estado"""
    colores = {
        'recibido': 'bg-info',
        'diagnostico': 'bg-warning text-dark',
        'presupuesto': 'bg-warning text-dark',
        'autorizada': 'bg-primary',
        'reparacion': 'bg-primary',
        'esperando_piezas': 'bg-secondary',
        'listo': 'bg-success',
        'entregada': 'bg-success',
        'cancelada': 'bg-danger'
    }
    color = colores.get(estado, 'bg-secondary')
    return f'<span class="badge {color}">{estado.title()}</span>'
