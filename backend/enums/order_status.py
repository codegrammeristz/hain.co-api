from enum import IntEnum


class OrderStatus(IntEnum):
    """Enum to describe the current status of order"""
    INCOMING = 1,
    ACCEPTED = 2,
    FULFILLED = 3
