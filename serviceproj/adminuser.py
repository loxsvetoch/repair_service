from serviceproj import db
from werkzeug.security import generate_password_hash
from serviceproj.models import Employee, Role


def create_admin_user():
    first_name = ""
    last_name = ""
    patronymic = ""
    salary = 100000
    service_id = 0
    phone = "77778889912"
    psw = "1111"
    # Ищем роль 'admin' в таблице Role
    role = Role.query.filter_by(role_name='admin').first()
    if role is None:
        print("Роль 'admin' не найдена в базе данных.")
        return
    # Хешируем пароль
    hash_pwd = generate_password_hash(psw)
    # Создаём нового сотрудника
    new_user = Employee(
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        salary=salary,
        service_id=service_id,
        phone_number=phone,
        password=hash_pwd,
        role_id=role.id  # Присваиваем идентификатор роли
    )
    # Добавляем пользователя в сессию и сохраняем в базе данных
    db.session.add(new_user)
    db.session.commit()
