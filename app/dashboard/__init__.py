"""
Blueprint del Dashboard
Resumen general del sistema
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .. import db
from ..models import Orden, Cliente, Equipo, Producto, Tecnico

bp = Blueprint('dashboard', __name__, template_folder='../../templates/dashboard')

@bp.route('/')
@login_required
def index():
    # Estadísticas principales
    stats = {
        'equipos_recibidos': Orden.query.filter_by(estado='recibido').count(),
        'en_reparacion': Orden.query.filter_by(estado='reparacion').count(),
        'esperando_piezas': Orden.query.filter_by(estado='esperando_piezas').count(),
        'listos': Orden.query.filter_by(estado='listo').count(),
        'entregados': Orden.query.filter_by(estado='entregada').count(),
        'clientes': Cliente.query.filter_by(activo=True).count(),
        'inventario_critico': Producto.query.filter(Producto.stock_actual <= Producto.stock_minimo).count(),
        'tecnicos_disponibles': Tecnico.query.filter_by(estado='disponible', activo=True).count(),
    }
    
    # Últimas órdenes
    ordenes_recientes = Orden.query.order_by(Orden.creado_en.desc()).limit(5).all()
    
    # Productos con stock crítico
    productos_criticos = Producto.query.filter(
        Producto.stock_actual <= Producto.stock_minimo
    ).limit(5).all()
    
    return render_template('dashboard/index.html', 
                         stats=stats, 
                         ordenes_recientes=ordenes_recientes,
                         productos_criticos=productos_criticos)
