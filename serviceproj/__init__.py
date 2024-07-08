from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret1111'
app.config['name_db_connect'] = 'admin'

# name_db_connect = 'admin'

# DataBase_connestion = {}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin_user:admin_password@localhost/servicebase'
# DataBase_connestion['admin'] = SQLAlchemy()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://employee_user:employee_password@localhost/servicebase'
# DataBase_connestion['employee'] = SQLAlchemy()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://client_user:client_password@localhost/servicebase'
# DataBase_connestion['client'] = SQLAlchemy()

login_manager = LoginManager()

# def dbs() -> SQLAlchemy:
#     return DataBase_connestion[app.config['name_db_connect']]

db = SQLAlchemy()


# Импорт моделей и представлений
from serviceproj.views.main import main_bp
from serviceproj.views.auth import auth_bp
from serviceproj.views.profile import profile_bp
from serviceproj.views.order import order_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(order_bp)

db.init_app(app)

