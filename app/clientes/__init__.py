"""
Blueprint de Clientes
CRUD completo, Historial, Búsqueda, Observaciones
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db
from ..models import Cliente, Equipo, Orden
from datetime import datetime

bp = Blueprint('clientes', __name__, template_folder='../../templates/clientes')

@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Cliente.query.filter_by(activo=True)
    
    if search:
        query = query.filter(
            (Cliente.nombre.ilike(f'%{search}%')) |
            (Cliente.numero_documento.ilike(f'%{search}%')) |
            (Cliente.telefono.ilike(f'%{search}%'))
        )
    
    clientes = query.order_by(Cliente.nombre).paginate(page=page, per_page=10)
    return render_template('clientes/index.html', clientes=clientes, search=search)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.form.get('nombre'),
            tipo_documento=request.form.get('tipo_documento'),
            numero_documento=request.form.get('numero_documento'),
            telefono=request.form.get('telefono'),
            email=request.form.get('email'),
            direccion=request.form.get('direccion'),
            ciudad=request.form.get('ciudad'),
            observaciones=request.form.get('observaciones')
        )
        
        try:
            db.session.add(cliente)
            db.session.commit()
            flash('Cliente creado exitosamente', 'success')
            return redirect(url_for('clientes.ver', id=cliente.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear cliente: {str(e)}', 'danger')
    
    return render_template('clientes/form.html', cliente=None, accion='crear')

@bp.route('/<int:id>')
@login_required
def ver(id):
    cliente = Cliente.query.get_or_404(id)
    equipos = Equipo.query.filter_by(cliente_id=id).all()
    return render_template('clientes/detalle.html', cliente=cliente, equipos=elevos)

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        cliente.nombre = request.form.get('nombre')
        cliente.tipo_documento = request.form.get('tipo_documento')
        cliente.numero_documento = request.form.get('numero_documento')
        cliente.telefono = request.form.get('telefono')
        cliente.email = request.form.get('email')
        cliente.direccion = request.form.get('direccion')
        cliente.ciudad = request.form.get('ciudad')
        cliente.observaciones = request.form.get('observaciones')
        cliente.actualizado_en = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Cliente actualizado exitosamente', 'success')
            return redirect(url_for('clientes.ver', id=cliente.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cliente: {str(e)}', 'danger')
    
    return render_template('clientes/form.html', cliente=cliente, accion='editar')

@bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.activo = False
    
    try:
        db.session.commit()
        flash('Cliente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cliente: {str(e)}', 'danger')
    
    return redirect(url_for('clientes.index'))

@bp.route('/<int:id>/historial')
@login_required
def historial(id):
    cliente = Cliente.query.get_or_404(id)
    ordenes = Orden.query.join(Equipo).filter(Equipo.cliente_id == id).order_by(Orden.creado_en.desc()).all()
    return render_template('clientes/historial.html', cliente=cliente, ordenes=ordenes)
