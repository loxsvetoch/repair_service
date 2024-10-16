#serviceproj/views/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash


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

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        patronymic = request.form.get('patronymic')
        phone = request.form.get('phone')
        psw = request.form.get('psw')
        psw_again = request.form.get('psw_again')

        if not (phone or psw or psw_again or patronymic or first_name or last_name):
            flash('Заполните все поля')
        elif psw != psw_again:
            flash('Введите одинаковые пароли')
        else:
            hash_pwd = generate_password_hash(psw)
            role = Role.query.filter_by(role_name='client').first()

            new_user = Client(phone_number=phone[1:],
                            first_name=first_name,
                            last_name=last_name,
                            patronymic=patronymic,
                            password=hash_pwd,
                            role=role.id
                            )   
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
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