from serviceproj import db
from flask_login import UserMixin


# Модель для клиентов
class Client(db.Model, UserMixin):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(11))
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    patronymic = db.Column(db.String(15))
    password = db.Column(db.String(200))
    role = db.Column(db.String(10)) 

# Модель для сотрудников
class Employee(db.Model, UserMixin):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    phone_number = db.Column(db.String(11))
    password = db.Column(db.String(200))
    salary = db.Column(db.Integer)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    role = db.Column(db.String(10))

# Модель для заказанных услуг
class OrderServices(db.Model):  
    __tablename__ = 'order_services'
    work_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)

# Модель для заказов
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    total_price = db.Column(db.Integer)
    date = db.Column(db.Date)

# Модель для списка услуг
class ServiceList(db.Model):
    __tablename__ = 'service_list'
    service_id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, primary_key=True)

# Модель для услуг
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(30))
    home_number = db.Column(db.Integer)
    box_index = db.Column(db.Integer)

# Модель для использованных компонентов
class UsedComponent(db.Model):
    __tablename__ = 'used_components'
    comp_id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, primary_key=True)
    counting = db.Column(db.Integer)

# Модель для мастерских услуг
class WorkshopService(db.Model):
    __tablename__ = 'workshop_services'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(40))
    description = db.Column(db.String(150))
    cost = db.Column(db.Integer)

# Модель для устройств
class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    type = db.Column(db.String(30))

# Модель для компонентов 
class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50))
    type = db.Column(db.String(30))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    cost = db.Column(db.Integer)