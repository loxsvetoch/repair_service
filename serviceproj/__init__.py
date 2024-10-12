# serviceproj/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret11111'
app.config['name_db_connect'] = 'admin'
#app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin_user:admin_password@localhost/servicebase'

login_manager = LoginManager()

db = SQLAlchemy()

#подключаем блюпринты
from serviceproj.views.main import main_bp
from serviceproj.views.auth import auth_bp
from serviceproj.views.profile import profile_bp
from serviceproj.views.order import order_bp
from serviceproj.views.repair import repair_bp

# регистрируем их
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(order_bp)
app.register_blueprint(repair_bp)

db.init_app(app)
from serviceproj.models import Client, Employee, Role, OrderServices, Order, ServiceList, Service,  WorkshopService, Device, ServiceDevice


def update_database():
    db_name = "servicebase"
    conn = psycopg2.connect(dbname=db_name, user="admin_user", password="admin_password", host="localhost")
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Проверяем, существует ли база данных
    cursor.execute(("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"), [db_name])
    exists = cursor.fetchone()
    
    if not exists:
        # Удаляем базу данных
        cursor.execute(f"DROP DATABASE {db_name}")
        print(f"База данных '{db_name}' удалена.")
        
        # Создаем новую базу данных
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"База данных '{db_name}' создана.")
        
    cursor.close()
    conn.close()


#with app.app_context():
#    update_database()  # Удаляем и создаем базу данных
#    db.create_all()     # Создаем таблицы по моделям

#from serviceproj.adminuser import create_admin_user
#with app.app_context():
#    create_admin_user()

#from serviceproj.fill_database import fill_device_components
#with app.app_context():
#    fill_device_components()