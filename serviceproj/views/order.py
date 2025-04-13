#serviceproj\views\order.py
from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql import func, text
import datetime

from serviceproj import db
from serviceproj.views.main import menu
from serviceproj.models import Device, ServiceDevice, Service, WorkshopService, ServiceList, Role, Order
order_bp = Blueprint('order', __name__)

def get_data():
    # Query the Device and WorkshopService models
    services = Service.query.all()
    print(services)

    #TODO девайсы только нужного сервиса по DeviceServices, услуги только по service_list
    devices = Device.query.all()
    workshop_services = WorkshopService.query.all()
    
    # Return the data as dictionaries or objects as needed
    return {
        "devices": devices,
        "workshop_services": workshop_services,
        "services" : services
    }

def get_filtered_data(service_id):
    devices = db.session.query(Device).join(ServiceDevice).filter(ServiceDevice.service_id == service_id).all()
    workshop_service_data = db.session.execute(text("SELECT * FROM get_workshop_services(:service_id)"), {'service_id': service_id}).fetchall()
    # Преобразуем данные в объекты WorkshopService потому что переделывать свойства на индексы
    workshop_services = [
        WorkshopService(id=ws[0], description=ws[1], cost=ws[2])
        for ws in workshop_service_data
    ]
    return {
        "devices": devices,
        "workshop_services": workshop_services
    }

@order_bp.route("/make_order", methods=['GET', 'POST'])
@login_required
def make_order():
    role = Role.query.filter_by(id=current_user.role_id).first()
    if role.role_name != "client":
        abort(403)

    if request.method == 'POST':
        service_idx = int(request.form.get("serviceAddress").split(" ")[-1])
        device_model = request.form.get("deviceModel")
        description = request.form.get("description")        
        service = Service.query.filter(Service.box_index==service_idx).first()
        device = Device.query.filter(Device.title==device_model).first()
        order = Order(
            service_id=service.id,
            client_id=current_user.id,
            device_id=device.id,
            total_price=0,
            date=func.now(),
            problem=description
        )
        db.session.add(order)
        db.session.commit()
    data = get_data()
    return render_template("order.html",
                            menu=menu,
                            services=data["services"],
                            devices=[],
                            workshop_services=[])

@order_bp.route("/filter_data", methods=['POST'])
def filter_data():
    service_address = request.form.get('serviceAddress')
    # Найти выбранный сервис по адресу
    selected_service = Service.query.filter_by(box_index=service_address.split(' ')[-1]).first()
    if not selected_service:
        return {'error': 'Service not found'}, 404
    # Получить устройства и услуги, связанные с выбранным сервисом
    filtered_data = get_filtered_data(selected_service.id)
    
    return {
        'devices': [{'title': d.title} for d in filtered_data['devices']],
        'workshop_services': [{'description': ws.description} for ws in filtered_data['workshop_services']]
    }
