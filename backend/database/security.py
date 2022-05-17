import string
import random
from cryptography.fernet import Fernet
from dotenv import dotenv_values

config = dotenv_values('.env')

fernet = Fernet('KnUnWaSL29SLlqz_F3m3QbRbb6Q8w8CuFFmLgDyClZE=')


def create_salt(length: int = 5) -> str:
    """A function to create a salt sequence to help with
    encrypting passwords

    :param int length: Length of the generated salt string, defaults to 5
    :return: A randomly generated salt string (5 characters)
    """
    salt = ''.join(random.choices(
        string.ascii_letters+string.digits,
        k=length
    ))
    return salt


def encrypt_password(password: str, salt: str) -> str:
    """A function to encrypt a password using the Fernet library using
    a predefined key

    :param str password: The password string to be encrypted
    :param str salt: The salt sequence to be used to increase security
    :return: Return the encrypted-decoded hash
    """
    pass_string = f'{salt}{password}'
    encrypted = fernet.encrypt(pass_string.encode())
    return encrypted.decode()


def decrypt_password(encrypted_password: str, salt: str) -> str:
    """Decrypts a password string with the salt and password string
    provided

    :param str encrypted_password: The encrypted password string from the
    database
    :param str salt: The salt sequence provided by the database column
    :return: The decrypted password
    """
    encrypted_password = encrypted_password.encode()
    decrypted = fernet.decrypt(encrypted_password).decode()
    decrypted = decrypted.replace(salt, '')
    return decrypted
