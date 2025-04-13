
CREATE OR REPLACE FUNCTION check_client(client_phone VARCHAR, client_password VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    client_exists BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1
        FROM clients
        WHERE phone_number = client_phone AND password = client_password
    ) INTO client_exists;

    RETURN client_exists;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION register_client(
    client_phone VARCHAR,
    client_password VARCHAR,
    client_first_name VARCHAR,
    client_last_name VARCHAR,
    client_patronymic VARCHAR,
    OUT success BOOLEAN
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Проверяем, существует ли клиент с таким номером телефона
    IF EXISTS (
        SELECT 1
        FROM clients
        WHERE phone_number = client_phone
    ) THEN
        -- Клиент уже существует
        success := FALSE;
    ELSE
        -- Вставляем нового клиента
        INSERT INTO clients (phone_number, password, first_name, last_name, patronymic, role_id)
        VALUES (
            client_phone,
            client_password,
            client_first_name,
            client_last_name,
            client_patronymic,
            (SELECT id FROM role WHERE role_name = 'client' LIMIT 1) -- Назначаем роль "client"
        );
        success := TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;

Добавить заказ и сервис
CREATE OR REPLACE FUNCTION public.add_order_and_service(p_service_id integer, p_client_id integer, p_device_id integer, p_description text, p_work_id integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
DECLARE
    order_id INTEGER;
BEGIN
    INSERT INTO "orders" (service_id, client_id, device_id, total_price, date, problem)
    VALUES (p_service_id, p_client_id, p_device_id, 0, NOW(), p_description);

    SELECT currval(pg_get_serial_sequence('"orders"', 'id')) INTO order_id;

    INSERT INTO "order_services" (order_id, work_id, status)
    VALUES (order_id, p_work_id, 'Ожидание');
    
END;
$function$
;

Создать дамп
CREATE OR REPLACE FUNCTION public.create_dump(dump_path text)
 RETURNS void
 LANGUAGE plsh
AS $function$
#!/bin/bash 
sudo -u postgres pg_dump -Fc -U postgres -d servicebase -f "$1"
$function$
;

Удалить дамп
CREATE OR REPLACE FUNCTION public.delete_dump(dump_path text)
 RETURNS void
 LANGUAGE plsh
AS $function$
#!/bin/bash
rm -f "$1"
$function$
;

Получить усуги сервиса по id
CREATE OR REPLACE FUNCTION public.get_workshop_services(service_id integer)
 RETURNS TABLE(id integer, description character varying, cost integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT ws.id, ws.description, ws.cost
    FROM workshop_services ws
    JOIN service_list sl ON ws.id = sl.work_id
    WHERE sl.service_id = get_workshop_services.service_id;
END;
$function$
;

логирование 
CREATE OR REPLACE FUNCTION public.log_trigger_operation()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO log (operation_type, table_name, record_id, new_data)
        VALUES ('INSERT', TG_TABLE_NAME, NEW.id, row_to_json(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO log (operation_type, table_name, record_id, old_data, new_data)
        VALUES ('UPDATE', TG_TABLE_NAME, NEW.id, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO log (operation_type, table_name, record_id, old_data)
        VALUES ('DELETE', TG_TABLE_NAME, OLD.id, row_to_json(OLD));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$function$
;

Регистрацияя
CREATE OR REPLACE FUNCTION public.register_client(client_phone character varying, client_password character varying, client_first_name character varying, client_last_name character varying, client_patronymic character varying, OUT success boolean)
 RETURNS boolean
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Проверяем, существует ли клиент с таким номером телефона
    IF EXISTS (
        SELECT 1
        FROM clients
        WHERE phone_number = client_phone
    ) THEN
        -- Клиент уже существует
        success := FALSE;
    ELSE
        -- Вставляем нового клиента
        INSERT INTO clients (phone_number, password, first_name, last_name, patronymic, role_id)
        VALUES (
            client_phone,
            client_password,
            client_first_name,
            client_last_name,
            client_patronymic,
            (SELECT id FROM role WHERE role_name = 'client' LIMIT 1) -- Назначаем роль "client"
        );
        success := TRUE;
    END IF;
END;
$function$
;


Обновить итоговую цену
CREATE OR REPLACE FUNCTION public.update_total_price()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Проверяем, что статус заказа стал "Выполнено"
    IF NEW.status = 'Выполнено' THEN
        -- Обновляем поле total_price в таблице orders
        UPDATE orders
        SET total_price = (
            SELECT SUM(ws.cost)  -- Используем правильное имя столбца
            FROM order_services os
            JOIN workshop_services ws ON os.work_id = ws.id
            WHERE os.order_id = NEW.id
        )
        WHERE id = NEW.id;
    END IF;

    RETURN NEW;
END;
$function$
;
