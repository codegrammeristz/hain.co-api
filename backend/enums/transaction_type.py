from enum import IntEnum


class TransactionType(IntEnum):
    """Enum to describe a transaction type


    ORDER (1): A transaction from the mobile application  \n
    BUY (2): A transaction from the walk in customers  \n
    ADMIN (3): Transactions done by admins
    """
    ORDER = 1
    BUY = 2
    ADMIN = 3
