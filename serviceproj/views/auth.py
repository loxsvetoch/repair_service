from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from serviceproj import app, db, login_manager
from serviceproj.models import Client, Employee


auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    # Здесь реализуйте код для загрузки пользователя из базы данных или хранилища по user_id
    return Client.query.get(int(user_id))  # Пример загрузки пользователя из SQLAlchemy

login_manager.init_app(app)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://employee_user:employee_password@localhost/servicebase'

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        patronymic = request.form.get('patronymic')
        phone = request.form.get('phone')
        psw = request.form.get('psw')
        psw_again = request.form.get('psw_again')

        if not (phone or psw or psw_again or patronymic or first_name or last_name):
            flash('Please, fill all fields!')
        elif psw != psw_again:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(psw)
            print(hash_pwd)
            print(len(hash_pwd))
            new_user = Client(phone_number=phone[1:],
                            first_name=first_name,
                            last_name=last_name,
                            patronymic=patronymic,
                            password=hash_pwd,
                            role_id="client"
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
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('profile.profile'))
            else:
                flash('Login or password is not correct')
        else:
            flash('Please fill login and password fields')

    return render_template('login.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))