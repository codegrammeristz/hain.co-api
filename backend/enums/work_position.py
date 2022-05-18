from enum import IntEnum


class CanteenPosition(IntEnum):
    """
    Enum describing canteen positions on the canteen.

    CHEF (1)
    CASHIER (2)
    SERVER (3)
    """
    CHEF = 1
    CASHIER = 2
    SERVER = 3


class AdminPosition(IntEnum):
    """Enum describing the Admin Position of an admin account.
    Defaults to 1

    SUPER_ADMIN (1): Type of admin with elevated privileges. All admins in the current and first
    release of the system will be a super admin
    SUB_ADMIN (2): Type of admin with limited privileges. Not used in the current iteration
    of the system
    """
    SUPER_ADMIN = 1
    SUB_ADMIN = 2
