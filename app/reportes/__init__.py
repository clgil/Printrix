"""
Blueprint del módulo - Placeholder para desarrollo futuro
"""

from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint(__name__.split('.')[-1], __name__, template_folder='../../templates/' + __name__.split('.')[-1])

@bp.route('/')
@login_required
def index():
    """Lista principal del módulo"""
    return render_template(f'{__name__.split(".")[-1]}/index.html')

@bp.route('/crear')
@login_required
def crear():
    """Formulario de creación"""
    return render_template(f'{__name__.split(".")[-1]}/form.html', accion='crear')
