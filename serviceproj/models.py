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

    # Связь с заказами
    orders = db.relationship('Order', backref='client', lazy=True)

# Модель для сотрудников
class Employee(db.Model, UserMixin):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    patronymic = db.Column(db.String(15))
    phone_number = db.Column(db.String(11))
    password = db.Column(db.String(200))
    salary = db.Column(db.Integer)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    role = db.Column(db.String(10))

    # Связь с услугами (местом работы)
    service = db.relationship('Service', backref='employees')

# Модель для заказов
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))  # Новое поле device_id
    total_price = db.Column(db.Integer)

    # Связь с заказанными услугами
    order_services = db.relationship('OrderServices', backref='order', lazy=True)
    used_components = db.relationship('UsedComponent', backref='order', lazy=True)
    
    # Связь с устройствами
    #device = db.relationship('Device', backref='orders')  # Связь с моделью Device

# Модель для заказанных услуг
class OrderServices(db.Model):  
    __tablename__ = 'order_services'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('workshop_services.id'), primary_key=True)
    date = db.Column(db.Date)

# Модель для списка услуг в мастерской
class ServiceList(db.Model):
    __tablename__ = 'service_list'
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('workshop_services.id'), primary_key=True)

# Модель для мастерских услуг
class WorkshopService(db.Model):
    __tablename__ = 'workshop_services'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150))
    cost = db.Column(db.Integer)

    # Связь с заказанными услугами
    orders = db.relationship('OrderServices', backref='workshop_service', lazy=True)
    service_lists = db.relationship('ServiceList', backref='workshop_service', cascade="all, delete-orphan")

# Модель для услуг
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(30))
    home_number = db.Column(db.Integer)
    box_index = db.Column(db.Integer)

    # Связь с заказами и сотрудниками
    orders = db.relationship('Order', backref='service', lazy=True)
    service_lists = db.relationship('ServiceList', backref='service', lazy=True)

# Модель для использованных компонентов
class UsedComponent(db.Model):
    __tablename__ = 'used_components'
    comp_id = db.Column(db.Integer, db.ForeignKey('components.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    count = db.Column(db.Integer)

# Модель для устройств
class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    type = db.Column(db.String(30))

    # Связь с компонентами
    components = db.relationship('Component', backref='device', lazy=True)

    # Связь с заказами
    #orders = db.relationship('Order', backref='device', lazy=True)  # Связь с моделью Order

# Модель для компонентов 
class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    cost = db.Column(db.Integer)

    # Связь с использованными компонентами
    used_in = db.relationship('UsedComponent', backref='component', lazy=True)
