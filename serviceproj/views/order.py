#serviceproj\views\order.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from serviceproj import db
from serviceproj.views.main import menu
from serviceproj.models import Component, Device, Service
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

@order_bp.route("/make_order", methods = ['GET', 'POST'])
@login_required
def make_order():
    
    print()
    return render_template("order.html", device_models=device_models, service_types=service_types, menu=menu)
