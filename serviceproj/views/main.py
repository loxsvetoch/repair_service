from flask import Blueprint, render_template, g
from flask_login import login_required

from serviceproj import app, db


main_bp = Blueprint('main', __name__)

menu = [
    {'name': 'Главная страница', 'url': "main.index"},
    {'name': 'Авторизация', 'url': "auth.login"},
    {'name': 'Регистрация', 'url': "auth.register"},
    {'name': 'Профиль', 'url': "profile.profile"},
    {'name': 'Сделать заказ', 'url': "order.make_order"}
]

@main_bp.route('/')
def index():
    return render_template('index.html',  menu = menu)
