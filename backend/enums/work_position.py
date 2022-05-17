from enum import IntEnum


class CanteenPosition(IntEnum):
    CHEF = 1
    CASHIER = 2
    SERVER = 3


class AdminPosition(IntEnum):
    SUPER_ADMIN = 1
    SUB_ADMIN = 2
