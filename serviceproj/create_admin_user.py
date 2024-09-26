
    first_name = "Андрей"
    last_name = "Сиделёв"
    patronymic = "Александрович"
    salary = 100000
    service_id = 0
    phone = "79780946953"
    psw = "1111"
    psw_again = "1111"
    role = "admin"
    hash_pwd = generate_password_hash(psw)

    new_user = Employee(first_name=first_name,
                    last_name=last_name, 
                    patronymic=patronymic, 
                    salary=salary,
                    service_id=service_id, 
                    phone_number=phone,   
                    password=hash_pwd, 
                    role=role)   
    
    db.session.add(new_user)
    db.session.commit()