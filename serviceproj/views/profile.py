#serviceproj\views\profile.py
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from serviceproj import db
from serviceproj.views.main import menu, admin_menu, employee_menu
from serviceproj.models import Employee, Service, WorkshopService, ServiceList

profile_bp = Blueprint('profile', __name__)

manage_type = ['Добавить', 'Удалить']

def get_orders_data():
    #TODO получение orders из сервиса id сервиса получить из current_user service id
    #Приведение к удобному json
    pass

@profile_bp.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    user = current_user
    #TODO изменение получения роли через Role.role_name WHERE id=id
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
    #TODO получение tasks из списка orders current сервиса
    tasks_data = [
        {"id": 1, "name": "Ремонт макбука", "date": "2024-09-29"},
    ]
    return render_template("employee_profile.html", menu = menu, tasks=tasks_data)

@profile_bp.route('/admin_profile',methods=["GET","POST"])
@login_required
def admin_profile(): 
    #TODO изменение получения роли по g
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
            # Логика добавления/обновления сервиса
            if todo == manage_type[0]:
                service_address = request.form.get('service_address')
                service_index = int(request.form.get('service_index'))
                service_number = int(request.form.get("service_number"))

                service = Service.query.filter_by(box_index=service_index).first()
                if not service:
                    #Добавить новый сервис
                    new_service = Service(
                        street = service_address,
                        home_number = service_number,
                        box_index = service_index,
                    )
                    db.session.add(new_service)
                    db.session.commit()
                    flash(f"Новый сервис добавлен")
                else:
                    #Обновить информацию о сервисе
                    db.session.query(Service.box_index == service_index).update(
                        street = service_address,
                        home_number = service_number,
                        box_index = service_index,
                    )

        #Услуги
        elif form_type == 'service_details_form':
            todo = request.form.get("stype") 
            # Логика добавления или удаления услуги сервиса
            if todo == manage_type[0]:
                
                service_idx = request.form.get("service_index_for_details") #!!!!!

                workshop_service_desc = request.form.get('service_description')
                price = int(request.form.get('service_price'))
                #получить id сервиса по почтовому индексу
                service_id = Service.query.filter_by(box_index=service_idx).first().id

                #добавление услуги
                workshop_service = WorkshopService(
                    description=workshop_service_desc,
                    cost=price
                )
                db.session.add(workshop_service)
                db.session.commit()
                
                #какая услуга у какого сервиса
                serv_list = ServiceList(
                    work_id=workshop_service.id,
                    service_id=service_id
                )
                db.session.add(serv_list)
                db.session.commit()

            elif todo == manage_type[1]:
                ws_id = request.form.get('ws_id')

                workshop_service = WorkshopService.query.get(ws_id)
                if workshop_service:
                    ServiceList.query.filter_by(work_id=ws_id).delete()
                    db.session.delete(workshop_service)
                    
                    db.session.commit()
                    flash("Услуга удалена")
                else:
                    flash("Услуга не найдена")

    return render_template("admin_profile.html",
                            menu=admin_menu,
                            manage_type=manage_type)