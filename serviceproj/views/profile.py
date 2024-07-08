from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    user = current_user
    if user.role == 'employee':
        return redirect(url_for('profile.employee_profile'))
    elif user.role == 'admin':
        return redirect(url_for('profile.admin_profile'))
    elif user.role == 'client':
        pass
    else:
        abort(403)

    user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'patronymic': user.patronymic
    }
    
    if request.method == "POST":
        # Здесь можно добавить обработку POST-запроса, если это необходимо
        # Например, обновление данных пользователя или обработка формы
        # Пример:
        # new_data = request.form.get('some_field')
        # user.some_field = new_data
        # db.session.commit()

        # После обработки POST-запроса можно выполнить перенаправление или другие действия

        return redirect(url_for('profile.profile'))  # Пример перенаправления

    return render_template('profile.html', user_data=user_data)

@profile_bp.route('/employee_profile', methods=["GET","POST"])
@login_required
def employee_profile():
    user = current_user
    if user.role != 'employee':
        abort(403)

    user_data = {
    'first_name': user.first_name,
    'last_name': user.last_name,
    'patronymic': user.patronymic
    }


    return render_template("EMPLOYEE PROFILEW")

@profile_bp.route('/admin_profile',methods=["GET","POST"])
@login_required
def admin_profile(): 
    user = current_user
    if user.role != 'admin':
        abort(403)
    user_data = {
    'first_name': user.first_name,
    'last_name': user.last_name,
    'patronymic': user.patronymic
    }

    return render_template("ADMIN PROFILE")