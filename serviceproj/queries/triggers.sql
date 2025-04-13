-- Active: 1727391738259@@127.0.0.1@5432@servicebase

CREATE TRIGGER clients_trigger_insert
AFTER INSERT ON public.clients FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER clients_trigger_update 
AFTER UPDATE ON public.clients FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER clients_trigger_delete
AFTER DELETE ON public.clients FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();


CREATE TRIGGER devices_trigger_insert
AFTER INSERT ON public.devices FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER devices_trigger_update 
AFTER UPDATE ON public.devices FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER devices_trigger_delete
AFTER DELETE ON public.devices FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();


CREATE TRIGGER employee_trigger_insert
AFTER INSERT ON public.employee FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER employee_trigger_update 
AFTER UPDATE ON public.employee FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER employee_trigger_delete
AFTER DELETE ON public.employee FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();

-- удалено
CREATE TRIGGER order_services_trigger_insert
AFTER INSERT ON public.order_services FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER order_services_trigger_update 
AFTER UPDATE ON public.order_services FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER order_services_trigger_delete
AFTER DELETE ON public.order_services FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();


CREATE TRIGGER orders_trigger_insert
AFTER INSERT ON public.orders FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER orders_trigger_update 
AFTER UPDATE ON public.orders FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER orders_trigger_delete
AFTER DELETE ON public.orders FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();


CREATE TRIGGER role_trigger_insert
AFTER INSERT ON public.role FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER role_trigger_update 
AFTER UPDATE ON public.role FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER role_trigger_delete
AFTER DELETE ON public.role FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();

-- удалено
CREATE TRIGGER service_device_trigger_insert
AFTER INSERT ON public.service_device FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER service_device_trigger_update 
AFTER UPDATE ON public.service_device FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER service_device_trigger_delete
AFTER DELETE ON public.service_device FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();

-- удалено
DROP TRIGGER service_list_trigger_insert
AFTER INSERT ON public.service_list FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
DROP TRIGGER service_list_trigger_update 
AFTER UPDATE ON public.service_list FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
DROP TRIGGER service_list_trigger_delete
AFTER DELETE ON public.service_list FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();


CREATE TRIGGER services_trigger_insert
AFTER INSERT ON public.services FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER services_trigger_update 
AFTER UPDATE ON public.services FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER services_trigger_delete
AFTER DELETE ON public.services FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();


CREATE TRIGGER workshop_services_trigger_insert
AFTER INSERT ON public.workshop_services FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER workshop_services_trigger_update 
AFTER UPDATE ON public.workshop_services FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();
CREATE TRIGGER workshop_services_trigger_delete
AFTER DELETE ON public.workshop_services FOR EACH ROW EXECUTE FUNCTION log_trigger_operation();