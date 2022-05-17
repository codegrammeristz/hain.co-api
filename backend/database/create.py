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


def add_admin_to_database(admin: Admin) -> Admin:
    cursor = pg_heroku.get_cursor()
    salt = create_salt()
    encrypted_password = encrypt_password(admin.admin_password, salt)
    try:
        sql = """INSERT INTO hainco_admin(
                    admin_full_name, 
                    admin_username, 
                    admin_position, 
                    admin_is_active,
                    admin_password_salt,
                    admin_password_hash
                    ) VALUES(%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (admin.admin_full_name,
                             admin.admin_username,
                             admin.admin_position,
                             admin.admin_is_active,
                             salt,
                             encrypted_password))
        pg_heroku.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        return admin


def add_customer_to_database(customer: Customer) -> Customer:
    cursor = pg_heroku.get_cursor()
    salt = create_salt()
    encrypted_password = encrypt_password(customer.customer_password, salt)
    try:
        sql = """INSERT INTO hainco_customer(
                    customer_first_name, 
                    customer_middle_name,
                    customer_last_name,
                    customer_email, 
                    customer_is_active,
                    customer_password_salt,
                    customer_password_hash,
                    customer_contact_number
                    ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (customer.customer_first_name,
                             customer.customer_middle_name,
                             customer.customer_last_name,
                             customer.customer_email,
                             customer.customer_is_active,
                             salt,
                             encrypted_password,
                             customer.customer_contact_number
                             ))
        pg_heroku.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        return customer


def add_product_to_database(product: Product) -> Product:
    cursor = pg_heroku.get_cursor()
    try:
        sql = """INSERT INTO hainco_product(
                    product_name, 
                    product_price,
                    product_image_link,
                    product_stock, 
                    product_type, 
                    product_is_active,
                    product_description,
                    product_code
                    ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (product.product_name,
                             product.product_price,
                             product.product_image_link,
                             product.product_stock,
                             product.product_type,
                             product.product_is_active,
                             product.product_description,
                             product.product_code
                             ))
        pg_heroku.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        return product


def add_staff_to_database(staff: Staff) -> Staff:
    cursor = pg_heroku.get_cursor()
    salt = create_salt()
    encrypted_password = encrypt_password(staff.staff_password, salt)
    try:
        sql = """INSERT INTO hainco_staff(
                        staff_full_name, 
                        staff_contact_number, 
                        staff_username, 
                        staff_password_salt,
                        staff_password_hash,
                        staff_address,
                        staff_position,
                        staff_is_active
                        ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (staff.staff_full_name,
                             staff.staff_contact_number,
                             staff.staff_username,
                             salt,
                             encrypted_password,
                             staff.staff_address,
                             staff.staff_position,
                             staff.staff_is_active
                             ))
        pg_heroku.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        return staff


def add_transaction_to_database(transaction: Transaction) -> Transaction:
    cursor = pg_heroku.get_cursor()
    try:
        sql = """INSERT INTO hainco_transaction(
                    transaction_agent, 
                    transaction_description, 
                    transaction_type, 
                    transaction_amount,
                    transaction_date
                    ) VALUES(%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (transaction.transaction_agent,
                             transaction.transaction_description,
                             transaction.transaction_type,
                             transaction.transaction_amount,
                             transaction.transaction_date
                             ))
        pg_heroku.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        return transaction
