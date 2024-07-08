from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

order_bp = Blueprint('order', __name__)

# Модели устройств
device_models = [
    'iPhone 13 Pro Max',
    'Samsung Galaxy S22 Ultra',
    'Xiaomi 12 Pro',
    'Realme GT Neo 3'
]

# Типы услуг
service_types = [
    'Ремонт',
    'Чистка',
    'Диагностика'
]

@login_required
@order_bp.route("/make_order", methods = ['GET', 'POST'])
def make_order():
    return render_template("order.html", device_models=device_models, service_types=service_types)