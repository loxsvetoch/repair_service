#serviceproj/views/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

from serviceproj import app, db, login_manager
from serviceproj.models import Client, Employee, Role

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(phone_number):
    if not phone_number:
        logout_user()
        return render_template('login.html')
    phone_number = session["phone_number"]
    user = Employee.query.filter_by(phone_number=phone_number).first()
    if user is None:
        user = Client.query.filter_by(phone_number=phone_number).first()
    return user

login_manager.init_app(app)

def register_client(phone, password, first_name, last_name, patronymic):
    query = text("""
        SELECT register_client(
            :phone,
            :password,
            :first_name,
            :last_name,
            :patronymic
        )
    """)
    # Выполняем запрос и возвращаем результат
    result = db.session.execute(query, {
        "phone": phone,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "patronymic": patronymic
    }).scalar()
    return result


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        patronymic = request.form.get('patronymic')
        phone = request.form.get('phone')
        psw = request.form.get('psw')
        psw_again = request.form.get('psw_again')

        # Проверяем, что все поля заполнены
        if not (phone and psw and psw_again and patronymic and first_name and last_name):
            flash('Заполните все поля')
        # Проверяем, что пароли совпадают
        elif psw != psw_again:
            flash('Введите одинаковые пароли')
        # Проверяем длину номера телефона
        elif not phone.isdigit() or len(phone) != 11:
            flash('Номер телефона должен содержать ровно 11 цифр (без символов и пробелов)')
        else:
            # Убираем '+' (если добавили это условие)
            phone = phone.lstrip('+')

            # Хэшируем пароль
            hashed_password = generate_password_hash(psw)

            try:
                # Вызываем функцию регистрации
                result = register_client(
                    phone=phone,
                    password=hashed_password,
                    first_name=first_name,
                    last_name=last_name,
                    patronymic=patronymic
                )

                if result:
                    flash('Регистрация прошла успешно!')
                    return redirect(url_for('auth.login'))
                else:
                    flash('Клиент с таким номером телефона уже существует')
            except Exception as e:
                print(f"Ошибка: {e}")
                flash('Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')[1:]
        password = request.form.get('password')

        if phone_number and password: 
            user = Client.query.filter_by(phone_number=phone_number).first()
            if not user:
                user = Employee.query.filter_by(phone_number=phone_number).first()
                
            if user and check_password_hash(user.password, password):
                login_user(user)
                session['phone_number'] = phone_number  # Сохраняем номер телефона
                return redirect(url_for('profile.profile'))
            else:
                flash('Логин или пароль некорректны')
        else:
            flash('Заполните все поля')

    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.app_errorhandler(401)
def handle_401(e):
    return render_template('unauthorized.html'), 401