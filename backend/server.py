from typing import Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from starlette import status
from starlette.exceptions import HTTPException

from backend.data_models import (
    Product,
    Staff,
    Customer,
    Admin, Transaction
)

from backend.database.database_operation import DatabaseOperator
import backend.database.database_operation as DB_STATIC
import backend.database.create as db_create
import backend.database.update as db_update
import backend.database.security as sec

app = FastAPI(
    title='Hain.co Web API',
    version='0.0.1',
    contact={
        'name': 'Clarence Rhey Salaveria',
        'email': 'clarencerhey.edu@gmail.com'
    }
)

# === TRUSTED HOSTS/REQUEST ORIGINS ===

origins = [
    'http://localhost:3000'
]

# === ADD MIDDLEWARE TO APPLICATION ===

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === TESTING ===

@app.get('/')
def root():
    """
    Root function to serve as gateway to the API when accessing it via the address
    """
    return {
        'message': 'Go to either of the links below to check the documentation',
        'links': {
            'ReDocs': 'https://hainco-api.herokuapp.com/redoc',
            'OpenAPI': 'https://hainco-api.herokuapp.com/docs'
        }

    }


# === PRODUCT ===

@app.get('/product',
         status_code=status.HTTP_200_OK)
def get_all_product() -> list[Product]:
    """
    Function to handle the endpoint to fetch all products from the database

    :return: Returns the list of Product objects fetched from the database
    """
    try:
        db = DatabaseOperator(cursor_factory=RealDictCursor)
        cursor = db.get_cursor()
        cursor.execute("""SELECT 
                            product_id,
                            product_name,
                            product_price,
                            product_image_link,
                            product_stock,
                            product_description,
                            product_type,
                            product_is_active,
                            product_code
                            FROM hainco_product""")
        all_product = cursor.fetchall()
        if not all_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No products exist'
            )
        return all_product
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.get('/product/{product_code}',
         status_code=status.HTTP_200_OK)
def get_product_by_product_code(product_code: str) -> Product:
    """
    Function to handle the endpoint to fetch a single product from the database by product code

    :return: Returns the Product object fetched
    """
    try:
        existing = False
        # check product if existing
        all_products = get_all_product()
        for record in all_products:
            # convert to a dictionary
            db_product = dict(record)
            if product_code == db_product['product_code']:
                existing = True
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product does not exist.'
            )
        db = DatabaseOperator(cursor_factory=RealDictCursor)
        cursor = db.get_cursor()
        cursor.execute(f"""SELECT 
                            product_id,
                            product_name,
                            product_price,
                            product_image_link,
                            product_stock,
                            product_description,
                            product_type,
                            product_is_active,
                            product_code
                            FROM hainco_product
                            WHERE product_code = '{product_code}'
                            """)
        product_record = cursor.fetchone()
        return product_record
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.post('/product/new_product',
          status_code=status.HTTP_201_CREATED)
def add_product(product: Product):
    """
    Function to handle the endpoint for adding a new product

    :param Product product: Pydantic model containing the product to be added
    :return: Returns the new product object and a message
    """
    try:
        code = product.product_code
        # check username if taken
        all_product = get_all_product()
        for record in all_product:
            # convert to a dictionary
            db_product = dict(record)
            if code == db_product['product_code']:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Username is already taken'
                )

        return {
            "data": db_create.add_product_to_database(product),
            "detail": "Product added to database"
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data format received'
        )


@app.put('/product/update_product/{current_product_code}',
         status_code=status.HTTP_200_OK)
def update_product(current_product_code: str, updated_product: Product) -> dict[str, dict[str, str] | str]:
    """
    Function to handle the endpoint for updating an Product object.

    :param str current_product_code: The current code of the Product to be updated
    :param Product updated_product: The Pydantic model containing the updated product info
    :return: Returns the updated Product object along with a message
    """
    try:
        existing = False
        # check product if existing
        all_products = get_all_product()
        for record in all_products:
            # convert to a dictionary
            db_product = dict(record)
            if current_product_code == db_product['product_code']:
                existing = True
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product does not exist.'
            )

        return {
            "data": db_update.update_product(current_product_code, updated_product),
            "detail": "Product updated to database"
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data format received'
        )


# === CANTEEN STAFF ===

@app.get('/staff',
         status_code=status.HTTP_200_OK)
def get_all_canteen_staff() -> list[Staff]:
    """
    Function to handle the endpoint to fetch all staffs from the database

    :return: Returns the list of Staff objects fetched from the database
    """
    try:
        db = DatabaseOperator(cursor_factory=RealDictCursor)
        cursor = db.get_cursor()
        cursor.execute("""SELECT 
                            staff_id,
                            staff_full_name,
                            staff_contact_number,
                            staff_username,
                            staff_address,
                            staff_position,
                            staff_is_active
                            FROM hainco_staff""")
        all_staff = cursor.fetchall()
        if not all_staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No staff records exist'
            )
        return all_staff
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.get('/staff/{username}',
         status_code=status.HTTP_200_OK)
def get_staff_by_username(username: str) -> dict[str | Any, str | Any]:
    """
    Function to handle the endpoint to fetch a single staff from the database by username

    :return: Returns the Staff object fetched
    """
    try:
        existing = False
        # check username if existing
        all_staff = get_all_canteen_staff()
        for record in all_staff:
            # convert to a dictionary
            db_staff = dict(record)
            if username == db_staff['staff_username']:
                existing = True
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Username does not exist.'
            )
        db = DatabaseOperator(cursor_factory=RealDictCursor)
        cursor = db.get_cursor()
        cursor.execute(f"""SELECT 
                            staff_id,
                            staff_full_name,
                            staff_contact_number,
                            staff_username,
                            staff_address,
                            staff_password_salt,
                            staff_password_hash,
                            staff_position,
                            staff_is_active
                            FROM hainco_staff
                            WHERE staff_username = '{username}'
                            """)
        staff_record = cursor.fetchone()
        # convert the result to a dictionary to modify its values
        staff_dict = dict(staff_record)
        # decrypt the password
        decrypted_password = sec.decrypt_password(
            staff_dict.get('staff_password_hash'),
            staff_dict.get('staff_password_salt')
        )
        # remove the hash and salt of the password
        staff_dict.pop('staff_password_hash')
        staff_dict.pop('staff_password_salt')
        # update with the actual password
        staff_dict.update({'staff_password': decrypted_password})
        # return the modified dictionary
        return staff_dict
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.post('/staff/new_staff',
          status_code=status.HTTP_201_CREATED)
def add_staff(staff: Staff):
    """
    Function to handle the endpoint for adding a new staff

    :param Staff staff: Pydantic model containing the staff to be added
    :return: Returns the new staff object and a message
    """
    try:
        username = staff.staff_username
        # check username if taken
        all_staff = get_all_canteen_staff()
        for record in all_staff:
            # convert to a dictionary
            db_staff = dict(record)
            if username == db_staff['staff_username']:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Username is already taken'
                )

        return {
            "data": db_create.add_staff_to_database(staff),
            "detail": "Staff added to database"
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data format received'
        )


@app.put('/staff/update_staff/{current_username}',
         status_code=status.HTTP_200_OK)
def update_staff(current_username: str, updated_staff: Staff) -> dict[str, dict[str, str] | str]:
    """
    Function to handle the endpoint for updating an Staff object.

    :param str current_username: The current username of the Staff to be updated
    :param Staff updated_staff: The Pydantic model containing the updated staff info
    :return: Returns the updated Staff object along with a message
    """
    try:
        existing = False
        # check product if existing
        all_staff = get_all_canteen_staff()
        for record in all_staff:
            # convert to a dictionary
            db_staff = dict(record)
            if current_username == db_staff['staff_username']:
                existing = True
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Staff does not exist.'
            )

        return {
            "data": db_update.update_staff(current_username, updated_staff),
            "detail": "Staff updated to database"
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data format received'
        )


# === CUSTOMER ===

@app.get('/customer',
         status_code=status.HTTP_200_OK)
def get_all_customer() -> list[Customer]:
    """
    Function to handle the endpoint to fetch all customers from the database

    :return: Returns the list of Customer objects fetched from the database
    """
    try:
        db = DatabaseOperator(cursor_factory=RealDictCursor)
        cursor = db.get_cursor()
        cursor.execute("""SELECT 
                            customer_id,
                            customer_first_name,
                            customer_middle_name,
                            customer_last_name,
                            customer_email,
                            customer_contact_number,
                            customer_is_active
                            FROM hainco_customer""")
        all_customer = cursor.fetchall()
        if not all_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No customer records exist'
            )
        return all_customer
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.get('/customer/{email}',
         status_code=status.HTTP_200_OK)
def get_customer_by_email(email: str):
    """
    Function to handle the endpoint to fetch a single customer from the database by email

    :return: Returns the Customer object fetched
    """
    try:
        existing = False
        # check username if existing
        all_customers = get_all_customer()
        for record in all_customers:
            # convert to a dictionary
            db_customer = dict(record)
            if email == db_customer['customer_email']:
                existing = True
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Account does not exist.'
            )
        db = DatabaseOperator(cursor_factory=RealDictCursor)
        cursor = db.get_cursor()
        cursor.execute(f"""SELECT 
                            customer_id,
                            customer_first_name,
                            customer_middle_name,
                            customer_last_name,
                            customer_email,
                            customer_password_salt,
                            customer_password_hash,
                            customer_contact_number,
                            customer_is_active
                            FROM hainco_customer
                            WHERE customer_email = '{email}'
                            """)
        customer_record = cursor.fetchone()
        # convert the result to a dictionary to modify its values
        customer_dict = dict(customer_record)
        # decrypt the password
        decrypted_password = sec.decrypt_password(
            customer_dict.get('customer_password_hash'),
            customer_dict.get('customer_password_salt')
        )
        # remove the hash and salt of the password
        customer_dict.pop('customer_password_hash')
        customer_dict.pop('customer_password_salt')
        # update with the actual password
        customer_dict.update({'customer_password': decrypted_password})
        # return the modified dictionary
        return customer_dict
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.post('/customer/new_customer',
          status_code=status.HTTP_201_CREATED)
def add_customer(customer: Customer) -> dict[str, Customer | str]:
    """
    Function to handle the endpoint for adding a new customer

    :param Customer customer: Pydantic model containing the customer to be added
    :return: Returns the new customer object and a message
    """
    try:
        email = customer.customer_email
        # check username if taken
        all_customers = get_all_customer()
        for record in all_customers:
            # convert to a dictionary
            db_customer = dict(record)
            if email == db_customer['customer_email']:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Email is already taken'
                )

        return {
            "data": db_create.add_customer_to_database(customer),
            "detail": "Customer added to database"
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data format received'
        )


@app.put('/customer/update_customer/{current_email}',
         status_code=status.HTTP_200_OK)
def update_customer(current_email: str, updated_customer: Customer) -> dict[str, dict[str, str] | str]:
    """
    Function to handle the endpoint for updating an Customer object.

    :param str current_email: The current email of the Customer to be updated
    :param Customer updated_customer: The Pydantic model containing the updated customer info
    :return: Returns the updated Customer object along with a message
    """
    try:
        existing = False
        # check product if existing
        all_customers = get_all_customer()
        for record in all_customers:
            # convert to a dictionary
            db_customer = dict(record)
            if current_email == db_customer['customer_email']:
                existing = True
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Customer does not exist.'
            )

        return {
            "data": db_update.update_customer(current_email, updated_customer),
            "detail": "Customer updated to database"
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data format received'
        )


# === ADMIN ===

@app.get('/admin',
         status_code=status.HTTP_200_OK)
def get_all_admin():
    """
    Function to handle the endpoint to fetch all admins from the database

    :return: Returns the list of Admin objects fetched from the database
    """
    try:
        db = DatabaseOperator(cursor_factory=RealDictCursor)
        cursor = db.get_cursor()
        cursor.execute("""SELECT 
                        admin_id,
                        admin_full_name,
                        admin_username,
                        admin_position,
                        admin_is_active
                        FROM hainco_admin""")
        all_admin = cursor.fetchall()
        if not all_admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No admin records found'
            )
        return all_admin
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.get('/admin/{username}',
         status_code=status.HTTP_200_OK)
def get_admin_by_username(username: str):
    """
    Function to handle the endpoint to fetch a single admin from the database by username

    :return: Returns the Admin object fetched
    """
    try:
        existing = False
        # check product if existing
        all_admins = get_all_admin()
        for record in all_admins:
            # convert to a dictionary
            db_admin = dict(record)
            if username == db_admin['admin_username']:
                existing = True
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product does not exist.'
            )
        db = DatabaseOperator(cursor_factory=RealDictCursor)
        cursor = db.get_cursor()
        cursor.execute(f"""SELECT 
                        admin_id,
                        admin_full_name,
                        admin_username,
                        admin_password_salt,
                        admin_password_hash,
                        admin_position,
                        admin_is_active
                        FROM hainco_admin
                        WHERE admin_username = '{username}'
                        """)
        admin_record = cursor.fetchone()
        # convert the result to a dictionary to modify its values
        admin_dict = dict(admin_record)
        # decrypt the password
        decrypted_password = sec.decrypt_password(
            admin_dict.get('admin_password_hash'),
            admin_dict.get('admin_password_salt')
        )
        # remove the hash and salt of the password
        admin_dict.pop('admin_password_hash')
        admin_dict.pop('admin_password_salt')
        # update with the actual password
        admin_dict.update({'admin_password': decrypted_password})
        # return the modified dictionary
        return admin_dict
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.post('/admin/new_admin',
          status_code=status.HTTP_201_CREATED)
def add_admin(admin: Admin):
    """
    Function to handle the endpoint for adding a new admin

    :param Admin admin: Pydantic model containing the admin to be added
    :return: Returns the new admin object and a message
    """
    try:
        username = admin.admin_username
        # check username if taken
        all_admin = get_all_admin()
        for record in all_admin:
            # convert to a dictionary
            db_admin = dict(record)
            if username == db_admin['admin_username']:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Username is already taken'
                )

        return {
            "data": db_create.add_admin_to_database(admin),
            "detail": "Admin added to database"
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data format received'
        )


@app.put('/admin/update_admin/{current_username}',
         status_code=status.HTTP_200_OK)
def update_admin(current_username: str, updated_admin: Admin) -> dict[str, dict[str, str] | str]:
    """
    Function to handle the endpoint for updating an Admin object.

    :param str current_username: The current username of the Admin to be updated
    :param Admin updated_admin: The Pydantic model containing the updated admin info
    :return: Returns the updated Admin object along with a message
    """
    try:
        existing = False
        # check product if existing
        all_admins = get_all_admin()
        for record in all_admins:
            # convert to a dictionary
            db_admin = dict(record)
            if current_username == db_admin['admin_username']:
                existing = True
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Admin does not exist.'
            )

        return {
            "data": db_update.update_admin(current_username, updated_admin),
            "detail": "Admin updated to database"
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


# === TRANSACTION ===

@app.get('/transaction',
         status_code=status.HTTP_200_OK)
def get_all_transaction() -> list[Transaction]:
    """
    Function to handle the endpoint to fetch all transactions from the database

    :return: Returns the list of Transaction objects fetched from the database
    """
    try:
        db = DatabaseOperator(cursor_factory=RealDictCursor)
        cursor = db.get_cursor()
        cursor.execute("""SELECT 
                        transaction_id,
                        transaction_agent,
                        transaction_description,
                        transaction_type,
                        transaction_amount,
                        transaction_date
                        FROM hainco_transaction""")
        all_transaction = cursor.fetchall()
        if not all_transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No transactions found'
            )
        return all_transaction
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )

# === RECORD ===
#
# @app.get('/record',
#          status_code=status.HTTP_200_OK)
# def get_all_record() -> list[Record]:
#     pass
#
#
# @app.get('/record/{id}')
# def get_record_by_id(id: int) -> Record:
#     pass
#
#
# # TODO change the id variable to properly match the database rows
# @app.post('/record/{id}')
# def add_record(id: int, updated_record: Record) -> Record:
#     pass


# === ORDERS ===
# TODO add the orders endpoints


# === META ===

@app.get('/meta/row_count')
def get_row_count() -> list[tuple]:
    """
    Counts the rows using the count_rows method in the DatabaseOperator class

    :return: Returns the tuples containing the table name and the corresponding row count
    """
    try:
        return DB_STATIC.count_rows()
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


# TODO add the authentication

# TODO add the email endpoint
