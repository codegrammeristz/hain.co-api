from enum import IntEnum


class ProductType(IntEnum):
    """Enum to describe the type of product, to be used with dropdowns in
    the client application
    """
    BREAKFAST = 1
    LUNCH = 2
    DESSERT = 3
    EXTRA = 4
