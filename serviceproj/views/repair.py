from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user
from serviceproj import db
from serviceproj.views.main import menu
from serviceproj.models import Component, Device, Service
repair_bp = Blueprint('order', __name__)

#получить информацию о девайсах и компонентах, и услугах этого сервиса
def get_data():
    db.session.execute()

@repair_bp.route("/close_order", methods = ['GET', 'POST'])
@login_required
def close_order():
    if current_user.role != 'employee':
        abort(403)
    
    
    return render_template("order.html", device_models='', service_types='', menu=menu)
