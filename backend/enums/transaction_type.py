from enum import IntEnum


class TransactionType(IntEnum):
    """Enum to describe a transaction type


    ORDER (int): A transaction from the mobile application  \n
    BUY (int): A transaction from the walk in customers  \n
    ADMIN (int): Transactions done by admins
    """
    ORDER = 1
    BUY = 2
    ADMIN = 3
