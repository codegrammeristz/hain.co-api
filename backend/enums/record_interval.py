from enum import IntEnum


class RecordInterval(IntEnum):
    """Enum to describe a interval (in days) the system will store,
    and try to generate a report
    """
    WEEKLY = 7
    BI_MONTHLY = 14
    MONTHLY = 30
