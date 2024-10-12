# serviceproj/views/repair.py
from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy import text
from serviceproj import db
from serviceproj.views.main import menu
from serviceproj.models import Order, Service, Role, WorkshopService, ServiceList

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
        {"description": ws[1], "cost": ws[2]}  # Убедитесь, что индексы правильные
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
    services = data.get('services', [])  # Извлекаем массив услуг

    print("Полученные услуги:", services)  # Проверяем, что получили
    #TODO принять order_id и добавлять новый order_services для каждой услуги
    #TODO Триггер для подсчета итогового заказа и изменения статуса на Выполено
    #TODO Фильтр заказов по дате по статусу "В ожидании"
    #TODO отображение выполненного заказа у клиента
    
    return redirect(url_for('profile.profile'))