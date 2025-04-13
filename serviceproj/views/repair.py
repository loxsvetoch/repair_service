# serviceproj/views/repair.py
from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy import text
from serviceproj import db
from serviceproj.views.main import menu
from serviceproj.models import Order, Service, Role, WorkshopService, ServiceList, OrderServices

repair_bp = Blueprint('repair', __name__)

@repair_bp.route("/close_order/<task_id>", methods=['GET', 'POST'])
@login_required
def close_order(task_id=None):
    user = current_user
    role = Role.query.filter_by(id=user.role_id).first()
    
    if role.role_name != 'employee':
        abort(403)

    if task_id is None:
        return render_template("unknown_order")
    
    order = Order.query.filter_by(id=task_id).first()

    if request.method == 'POST':
        # Получаем данные из запроса
        data = request.form.getlist('serviceType')  # Получаем список услуг
        print(data)
    return render_template("repair.html", menu=menu, order=order)


@repair_bp.route("/filter_workshop_services/", methods=['POST'])
@login_required
def filter_workshop_services():
    user = current_user
    role = Role.query.filter_by(id=user.role_id).first()
    if role.role_name != 'employee':
        abort(403)
    workshop_service_data = db.session.execute(text("SELECT * FROM get_workshop_services(:service_id)"), {'service_id': current_user.service_id}).fetchall()
    workshop_services = [
        {"description": ws[1], "cost": ws[2]} 
        for ws in workshop_service_data
    ]
    return jsonify(workshop_services)

@repair_bp.route("/calc_order/", methods=['GET', 'POST'])
@login_required
def calc_order(data=None):
    user = current_user
    role = Role.query.filter_by(id=user.role_id).first()
    if role.role_name != 'employee':
        abort(403)
    data = request.get_json()  # Получаем данные из POST-запроса
    services = data.get('services', [])
    order_id = data.get('order_id', [])

    OrderServices.query.filter_by(order_id=order_id).delete()
    for work in services:
        work = " ".join(work.split(" ")[:-1])
        print(work)
        work_id = WorkshopService.query.filter(WorkshopService.description == work).first().id
        new_order_service = OrderServices(
            order_id=order_id,
            work_id=work_id
        )          
        db.session.add(new_order_service)
    db.session.commit()

    db.session.query(Order).filter(Order.id == order_id).update(
        {'status': 'Выполнено'}
    )
    db.session.commit()

    #TODO отображение выполненного заказа у клиента
    
    return redirect(url_for('profile.profile'))