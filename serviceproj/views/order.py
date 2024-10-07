#serviceproj\views\order.py
from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user
from serviceproj import db
from serviceproj.views.main import menu
from serviceproj.models import Device, Service, WorkshopService, Role
order_bp = Blueprint('order', __name__)


def get_data():
    # Query the Device and WorkshopService models
    services = Service.query.all()

    #TODO девайсы только нужного сервиса по DeviceServices, услуги только по service_list
    devices = Device.query.all()
    workshop_services = WorkshopService.query.all()
    

    # Return the data as dictionaries or objects as needed
    return {
        "devices": devices,
        "workshop_services": workshop_services,
        "services" : services
    }

@order_bp.route("/make_order", methods = ['GET', 'POST'])
@login_required
def make_order():
    #TODO изменение получения роли
    role = Role.query.filter_by(id=current_user.role_id).first()
    if role.role_name != "client":
        abort(403)

    #TODO
    # формируется заказ в таблице order 
    # добавить поле для total cost(после выполнения заказа считает триггер, собирая цену всех услуг)
    # после этого формируеться запись в order_services => добавляется в ЛК employee соответствующего service
    # + добавить в OrderServices или в order поле status. так же добавить устройство из таблицы devices 

    #TODO
    # Вообще убрать тип услуги из оформления заказа. Услуги добавляет работник после выполнения, смотря ан проблему
    

    data=get_data()
    return render_template("order.html",
                            menu=menu,
                            services=data["services"],
                            devices=data["devices"],
                            workshop_services= data["workshop_services"])