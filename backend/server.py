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
    return {'message': 'Hello World'}


# === PRODUCT ===

@app.get('/product',
         status_code=status.HTTP_200_OK)
def get_all_product() -> list[Product]:
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
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.get('/product/{product_code}')
def get_product_by_product_code(product_code: str):
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


@app.post('/product/new_product')
def add_product(product: Product):
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


@app.put('/product/update_product/{current_product_code}')
def update_product(current_product_code: str, updated_product: Product):
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
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.get('/staff/{username}',
         status_code=status.HTTP_200_OK)
def get_staff_by_username(username: str):
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
def update_staff(current_username: str, updated_staff: Staff):
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
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


@app.get('/customer/{email}',
         status_code=status.HTTP_200_OK)
def get_customer_by_email(email: str):
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
def add_customer(customer: Customer):
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
def update_customer(current_email: str, updated_customer: Customer):
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
def update_admin(current_username: str, updated_admin: Admin):
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


@app.get('/transaction/{id}',
         status_code=status.HTTP_200_OK)
def get_transaction_by_id(id: int) -> Transaction:
    pass


@app.post('/transaction/{id}',
          status_code=status.HTTP_201_CREATED)
def add_transaction(id: int, transaction: Transaction) -> Transaction:
    pass


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


# === META ===

@app.get('/meta/row_count')
def get_row_count():
    try:
        return DB_STATIC.count_rows()
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Failed to connect to database'
        )


if __name__ == '__main__':
    print(get_admin_by_username('eluxify'))
