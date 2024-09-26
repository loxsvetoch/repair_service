#serviceproj\views\profile.py
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from serviceproj import db
from serviceproj.views.main import menu, admin_menu, employee_menu
from serviceproj.models import Employee, Service, WorkshopService

profile_bp = Blueprint('profile', __name__)

manage_type = ['Добавить', 'Удалить']

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

    return render_template('profile.html', user_data=user_data, menu = menu)

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

    return render_template("employee_profile.html", menu = menu)

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
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'employee_form':
            employee_number = request.form.get("employee_number")
            if employee_number[0] == "+":
                employee_number = employee_number[1:]
            #Получить тип действия (Добавить/удалить)
            todo = request.form.get("stype") 

            employee_first_name = request.form.get('employee_first_name')
            employee_last_name = request.form.get('employee_last_name')
            employee_patronymic = request.form.get('employee_patronymic')
            employee_salary = int(request.form.get('employee_salary'))
            employee_service_id = request.form.get('employee_service_id')
            employee_password = request.form.get('employee_password')
            # Логика добавления/изменения или удаления работника
            employee = Employee.query.filter_by(phone_number=employee_number).first()
            if todo == manage_type[0]:
                # Добавление/Изменение работника
                if not employee:
                    new_employee = Employee(first_name = employee_first_name,
                        last_name =employee_last_name,
                        patronymic = employee_patronymic,
                        phone_number = employee_number,
                        password = generate_password_hash(employee_password),
                        salary = employee_salary,
                        service_id = employee_service_id,
                        role = "employee")
                    db.session.add(new_employee)
                    db.session.commit()
                    flash(f"Новый работник {employee_first_name} {employee_last_name} добавлен")
                else:
                    #Если работник есть то обновляем по новым данным
                    db.session.query(Employee).filter(Employee.phone_number == employee_number).update(
                        {   "first_name" : employee_first_name,
                            "last_name" : employee_last_name,
                            "patronymic" : employee_patronymic,
                            "phone_number" : employee_number, 
                            "password": generate_password_hash(employee_password),
                            "salary": employee_salary,
                            "service_id": employee_service_id}
                    )
            elif todo == manage_type[1]:
                # Логика удаления работника
                Employee.query.filter(Employee.phone_number==employee_number).delete()
                flash("Работник уничтожен")

        elif form_type == 'service_form':
            #Получить тип действия (Добавить/удалить)
            todo = request.form.get("stype") 
            service_address = request.form.get('service_address')
            service_index = int(request.form.get('service_index'))
            service_number = int(request.form.get("service_number"))
            service_specialization = request.form.get("service_specialization")

            service = Service.query.filter_by(service_index=service_index).first()

            if todo == manage_type[0]:
                if not service:
                    #Добавить новый сервис
                    new_service = Service(
                        street = service_address,
                        home_number = service_number,
                        box_index = service_index,
                        specialization = service_specialization
                    )
                    db.session.add(new_service)
                    db.session.commit()
                    flash(f"Новый сервис {service_specialization} добавлен")
                else:
                    #Обновить информацию о сервисе
                    db.session.query(Service.box_index == service_index).update(
                        street = service_address,
                        home_number = service_number,
                        box_index = service_index,
                        specialization = service_specialization
                    )

            elif todo == manage_type[1]:
                # Логика удаления сервиса
                Service.query.filter_by(box_index=service_index)
                flash("Сервис уничтожен")

        elif form_type == 'service_details_form':
            #Получить тип действия (Добавить/удалить)
            #Услугу можно только добавить или удалить
            todo = request.form.get("stype") 
            
            service_idx = request.form.get("service_index_for_details") #!!!!!
            workshop_service_name = request.form.get('service_name')

            workshop_service_desc = request.form.get('service_description')
            price = request.form.get('service_price')
            ws_id = request.get(" ws_id")
            # Логика добавления или удаления услуги сервиса
            if todo == manage_type[0]:
                #добавление услуги
                #TODO триггер на создание сопоставления в таблице service_list 
                workshop_service = WorkshopService(
                    description=workshop_service_desc,
                    cost=price
                )
                db.session.add(workshop_service)
            elif todo == manage_type[1]:
                #удаление услуги
                WorkshopService.query.filter(WorkshopService.id==ws_id).delete()
                flash("услуга удалена")

    return render_template("admin_profile.html",
                            menu=admin_menu,
                            manage_type=manage_type)