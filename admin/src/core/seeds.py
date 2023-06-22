"""Module to create automatic database seeding
"""
from src.core import seeds
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def run():
    """Inserts 3 members and default system congi
    """
    # Add data by default

    db.engine.execute(
        """ INSERT INTO public.discipline (id, name, category, coach, schedule, monthly_price, active, created_at) VALUES (1, 'Tiro al Blanco', 'Armas', 'Pablo', '15:30', '1500', true, '2023-06-20 20:10:10.532682');
            INSERT INTO public.discipline (id, name, category, coach, schedule, monthly_price, active, created_at) VALUES (2, 'Salto en alto', 'Atletismo', 'Marcela', '18:30', '1500', true, '2023-06-20 21:20:51.159135');

            INSERT INTO public.member (id, first_name, last_name, personal_id_type, personal_id, gender, address, membership_state, phone_number, email, activation_date, profile_photo_name) VALUES (1, 'Nicolas', 'Barone', 'DNI', '25986745', 'Masculino', 'vazquez diez 18', true, '2364598874', 'nicolasbarone@gmail.com', '2023-06-20 18:17:26.941431', NULL);

            INSERT INTO public.invoice (id, year, month, base_price, total_price, paid, member_id, expired, receipt_photo_name) VALUES (1, 2023, 6, '100', 1760, true, 1, true, NULL);


      

            INSERT INTO public.invoice_extra_item (id, description, amount, payment_date, discipline_id, invoice_id) VALUES (1, 'Cuota de Tiro al Blanco por el monto de 1500', 1500, '2023-06-20 23:30:03.734234', 1, 1);
            INSERT INTO public.invoice_extra_item (id, description, amount, payment_date, discipline_id, invoice_id) VALUES (2, 'Recargo de 160.0 por vencimiento de factura 6/2023', 160, '2023-06-20 23:30:05.802516', NULL, 1);


          

            INSERT INTO public.member_discipline (member_id, discipline_id, updated_at, created_at) VALUES (1, 1, '2023-06-20 18:17:26.95927', '2023-06-20 18:17:26.959294');



            INSERT INTO public.payment (id, invoice_id, member_id, amount, payment_date) VALUES (1, 1, 1, '1760.0', '2023-06-20 23:30:08.505355');


        

            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (1, 'users_index', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (2, 'users_create', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (3, 'users_destroy', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (4, 'users_show', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (5, 'users_edit', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (6, 'discipline_index', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (7, 'discipline_create', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (8, 'discipline_update', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (9, 'discipline_destroy', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (10, 'discipline_show', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (11, 'member_index', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (12, 'member_create', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (13, 'member_update', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (14, 'member_destroy', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (15, 'member_show', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (16, 'payment_index', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (17, 'payment_show', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (18, 'payment_update', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');
            INSERT INTO public.permissions (id, name, updated_at, created_at) VALUES (19, 'system_config_show', '2023-06-20 18:22:26.410681', '2023-06-20 18:22:26.410681');



            INSERT INTO public.role (id, name, updated_at, created_at) VALUES (1, 'Administrador', NULL, NULL);
            INSERT INTO public.role (id, name, updated_at, created_at) VALUES (2, 'Operador', NULL, NULL);
            INSERT INTO public.role (id, name, updated_at, created_at) VALUES (3, 'Socio', NULL, NULL);



            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (19, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (1, 2, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (2, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (3, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (4, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (5, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (6, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (7, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (8, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (9, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (10, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (11, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (12, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (13, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (14, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (15, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (16, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (17, 1, NULL, NULL);
            INSERT INTO public.role_permissions (permission_id, role_id, updated_at, created_at) VALUES (18, 1, NULL, NULL);



            INSERT INTO public.system_config (id, items_qty_for_grids, public_payments_available, public_contact_info_available, payment_header_text, base_monthly_fee, delayed_payment_interests_rate, updated_at, inserted_at) VALUES (1, 10, false, false, 'This is a header', 100, 0.1, NULL, NULL);



            INSERT INTO public."user" (id, firstname, lastname, username, email, active, password, updated_at, created_at) VALUES (1, 'David', 'Franco', 'dafranco', 'francodavid20@gmail.com', true, 'justatest', NULL, NULL);
            INSERT INTO public."user" (id, firstname, lastname, username, email, active, password, updated_at, created_at) VALUES (2, 'Victor', 'Hugo', 'morales', 'morales@gmail.com', true, 'justatest', NULL, NULL);
            INSERT INTO public."user" (id, firstname, lastname, username, email, active, password, updated_at, created_at) VALUES (3, 'Nicolas', 'Barone', 'nicob', 'nicolasbarone@gmail.com', true, '123', NULL, NULL);


            INSERT INTO public.user_role (user_id, role_id, updated_at, created_at) VALUES (1, 1, NULL, NULL);
            INSERT INTO public.user_role (user_id, role_id, updated_at, created_at) VALUES (1, 2, NULL, NULL);
            INSERT INTO public.user_role (user_id, role_id, updated_at, created_at) VALUES (2, 2, NULL, NULL);
            INSERT INTO public.user_role (user_id, role_id, updated_at, created_at) VALUES (3, 1, NULL, NULL);
            INSERT INTO public.user_role (user_id, role_id, updated_at, created_at) VALUES (3, 2, NULL, NULL);



            SELECT pg_catalog.setval('public.discipline_id_seq', 2, true);



            SELECT pg_catalog.setval('public.invoice_extra_item_id_seq', 2, true);


          

            SELECT pg_catalog.setval('public.invoice_id_seq', 1, true);


         

            SELECT pg_catalog.setval('public.member_id_seq', 1, true);


        

            SELECT pg_catalog.setval('public.payment_id_seq', 1, true);
            SELECT pg_catalog.setval('public.permissions_id_seq', 19, true);



            SELECT pg_catalog.setval('public.role_id_seq', 3, true);



            SELECT pg_catalog.setval('public.system_config_id_seq', 1, true);



            SELECT pg_catalog.setval('public.user_id_seq', 3, true);
            """)
