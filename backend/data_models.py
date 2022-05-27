from pydantic import BaseModel, validator
from typing import Optional
import datetime as dt

# enum types
from backend.enums.product_type import ProductType
from backend.enums.transaction_type import TransactionType
from backend.enums.work_position import CanteenPosition, AdminPosition
from backend.enums.order_status import OrderStatus


class Customer(BaseModel):
    customer_first_name: str
    customer_middle_name: Optional[str]
    customer_last_name: str
    customer_password: str
    customer_email: str
    customer_contact_number: str
    customer_is_active: bool


class Staff(BaseModel):
    staff_full_name: str
    staff_contact_number: str
    staff_username: str
    staff_password: str
    staff_position: CanteenPosition
    staff_is_active: bool


class Admin(BaseModel):
    admin_full_name: str
    admin_username: str
    admin_password: str
    admin_position: AdminPosition
    admin_is_active: bool


class Product(BaseModel):
    product_name: str
    product_price: float
    product_image_link: str
    product_stock: int
    product_description: str
    product_type: ProductType
    product_is_active: bool
    product_code: str


class Transaction(BaseModel):
    transaction_agent: str
    transaction_description: str
    transaction_type: TransactionType
    transaction_amount: Optional[float]
    transaction_date: dt.datetime


class Order(BaseModel):
    order_product_code: str
    order_customer_email: str
    order_request: str
    order_date: Optional[dt.datetime]
    order_staff_username: str
    order_status: OrderStatus

    @validator('order_date', pre=True, always=True)
    def set_ts_now(cls, v):
        return v or dt.datetime.now()