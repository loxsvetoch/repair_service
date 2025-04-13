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
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

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
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # Связь с услугами (местом работы)
    service = db.relationship('Service', backref='employees')

# Модель для ролей (роль пользователя)
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20))

    # Связь с сотрудниками и клиентами
    employees = db.relationship('Employee', backref='role', lazy=True)
    clients = db.relationship('Client', backref='role', lazy=True)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))  # Поле device_id
    total_price = db.Column(db.Integer)
    date = db.Column(db.Date)
    problem = db.Column(db.String(255))
    status = db.Column(db.String(30), default="Ожидание")

    # Связь с заказанными услугами
    order_services = db.relationship('OrderServices', backref='order', lazy=True)


# Модель для заказанных услуг
class OrderServices(db.Model):  
    __tablename__ = 'order_services'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('workshop_services.id'), primary_key=True)

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

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    type = db.Column(db.String(30))

    service_lists = db.relationship('ServiceDevice', backref='device', lazy=True)

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(30))
    home_number = db.Column(db.Integer)
    box_index = db.Column(db.Integer)
    specialization = db.Column(db.String(50))

    device_lists = db.relationship('ServiceDevice', backref='service', lazy=True)

#ремонт каких девайсов поддерживает сервис
class ServiceDevice(db.Model):
    __tablename__ = 'service_device'
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), primary_key=True)
