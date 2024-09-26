from flask import Blueprint, render_template, g
from flask_login import login_required

from serviceproj import app, db

from serviceproj.models import Employee, Service
from serviceproj import db
from werkzeug.security import check_password_hash, generate_password_hash

import glob
images = glob.glob("serviceproj\static\images\*jpg")
main_bp = Blueprint('main', __name__)


menu = [
    {'name': 'Repair service', 'url': "main.index"},
    {'name': 'Авторизация', 'url': "auth.login"},
    {'name': 'Регистрация', 'url': "auth.register"},
    {'name': 'Профиль', 'url': "profile.profile"},
    {'name': 'Сделать заказ', 'url': "order.make_order"}
]

employee_menu = [
    {'name': 'Repair service', 'url': "main.index"},
    {'name': 'Авторизация', 'url': "auth.login"},
    {'name': 'Регистрация', 'url': "auth.register"},
    {'name': 'Профиль', 'url': "profile.profile"},
    {'name': 'Сделать заказ', 'url': "order.make_order"}
]

admin_menu = [
    {'name': 'Repair service', 'url': "main.index"},
    {'name': 'Авторизация', 'url': "auth.login"},
    {'name': 'Регистрация', 'url': "auth.register"},
    {'name': 'Профиль', 'url': "profile.profile"},
    {'name': 'Сделать заказ', 'url': "order.make_order"}
]

@main_bp.route('/')
def index():
    return render_template('index.html',  menu = menu, images = images)

