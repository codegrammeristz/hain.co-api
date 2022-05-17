import psycopg2

from database.security import decrypt_password
from database_operation import DatabaseOperator


def login(username: str, password: str) -> bool:
    """
    get row from matching username
    get salt
    get hashed password
    decrypt password
    compare password with entered
    return True if correct,
    return False if not
    """
    pass