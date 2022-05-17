import psycopg2

from backend.data_models import (
    Admin,
    Customer,
    Product,
    Staff,
    Transaction,
)
from backend.database.security import create_salt, encrypt_password
from backend.database.database_operation import DatabaseOperator

pg_heroku = DatabaseOperator()


def update_admin(current_username: str, updated_admin: Admin):
    cursor = pg_heroku.get_cursor()
    salt = create_salt()
    encrypted_password = encrypt_password(updated_admin.admin_password, salt)
    try:
        sql = f"""UPDATE hainco_admin
                    SET admin_full_name = %s,
                    admin_username = %s,
                    admin_position = %s, 
                    admin_is_active = %s,
                    admin_password_salt = %s,
                    admin_password_hash = %s
                    WHERE admin_username = '{current_username}'
                    """
        cursor.execute(sql, (updated_admin.admin_full_name,
                             updated_admin.admin_username,
                             updated_admin.admin_position,
                             updated_admin.admin_is_active,
                             salt,
                             encrypted_password))
        pg_heroku.commit()
        cursor.close()
        return {'message': 'Record updated!'}
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)


def update_product(current_product_code: str, updated_product: Product):
    cursor = pg_heroku.get_cursor()
    try:
        sql = f"""UPDATE hainco_product
                    SET product_name = %s, 
                    product_price = %s,
                    product_image_link = %s,
                    product_stock = %s, 
                    product_type = %s, 
                    product_is_active = %s,
                    product_description = %s,
                    product_code = %s
                    WHERE product_code = '{current_product_code}'
                    """
        cursor.execute(sql, (updated_product.product_name,
                             updated_product.product_price,
                             updated_product.product_image_link,
                             updated_product.product_stock,
                             updated_product.product_type,
                             updated_product.product_is_active,
                             updated_product.product_description,
                             updated_product.product_code
                             ))

        pg_heroku.commit()
        cursor.close()
        return {'message': 'Record updated!'}
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)


def update_staff(current_username: str, updated_staff: Staff):
    cursor = pg_heroku.get_cursor()
    salt = create_salt()
    encrypted_password = encrypt_password(updated_staff.staff_password, salt)
    try:
        sql = f"""UPDATE hainco_staff
                    SET staff_full_name = %s, 
                        staff_contact_number = %s, 
                        staff_username = %s, 
                        staff_password_salt = %s,
                        staff_password_hash = %s,
                        staff_address = %s,
                        staff_position = %s,
                        staff_is_active = %s
                    WHERE staff_username = '{current_username}'
                    """
        cursor.execute(sql, (updated_staff.staff_full_name,
                             updated_staff.staff_contact_number,
                             updated_staff.staff_username,
                             salt,
                             encrypted_password,
                             updated_staff.staff_address,
                             updated_staff.staff_position,
                             updated_staff.staff_is_active))
        pg_heroku.commit()
        cursor.close()
        return {'message': 'Record updated!'}
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)


def update_customer(current_email: str, updated_customer: Customer):
    cursor = pg_heroku.get_cursor()
    salt = create_salt()
    encrypted_password = encrypt_password(updated_customer.customer_password, salt)
    try:
        sql = f"""UPDATE hainco_customer
                    SET customer_first_name = %s, 
                        customer_middle_name = %s,
                        customer_last_name = %s,
                        customer_email = %s, 
                        customer_is_active = %s,
                        customer_password_salt = %s,
                        customer_password_hash = %s,
                        customer_contact_number = %s
                    WHERE customer_email = '{current_email}'
                    """
        cursor.execute(sql, (updated_customer.customer_first_name,
                             updated_customer.customer_middle_name,
                             updated_customer.customer_last_name,
                             updated_customer.customer_email,
                             updated_customer.customer_is_active,
                             salt,
                             encrypted_password,
                             updated_customer.customer_contact_number
                             ))
        pg_heroku.commit()
        cursor.close()
        return {'message': 'Record updated!'}
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)