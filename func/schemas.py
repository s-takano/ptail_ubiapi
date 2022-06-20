from pydantic import BaseModel, validator
from typing import Optional, List

"""
Contains all schemas alias domain models of the application.
For domain modelling, the library pydantic is used.
Pydantic allows to create versatile domain models and ensures data integrity and much more.
"""


class CalculationOption(BaseModel):
    tax_rounding_mode: str  # "down",
    price_rounding_mode: str  # "plain",
    tax_calculation_level: str  # "checkout"

    class Config:
        fields = {
            "tax_rounding_mode": {"description": "down"},
            "price_rounding_mode": {"description": "plain"},
            "tax_calculation_level": {"description": "checkout"}
        }

class CheckoutPayment(BaseModel):
    ...

class CheckoutItem(BaseModel):
    ...

class CheckoutTax(BaseModel):
    ...

class CheckoutBase(BaseModel):
    """
    Checkout base schema
    """
    guid: str  # "8928309238-d987aerkeh-9847tdfkzhg4"
    device_id: str  # "710b52d6-9d8f-11e5-9aac-af957c6aaf43"
    account_id: int  # 1
    paid_at: str  # "2011-12-24T16:20:20Z"
    sales_date: str  #: "2011-12-25"
    price: str  # "385.0",
    change: str  # "4000.0"
    status: str  # "close"
    # cashier_id: Optional[int] # null
    customers_count: int  # 0
    payments: List[CheckoutPayment]  # "[ $Payments]
    taxes: List[CheckoutTax]  # "[ $CheckoutTaxes]
    items: List[CheckoutItem]  # " [ $CheckoutItems]
    # table_ids : List[int] #" [99, 8]
    customer_tag_ids: List[int]  # [10, 1003]
    # modifier": "0.0",
    calculation_option: CalculationOption

    class Config:
        fields = {
            "guid": {"description": "8928309238-d987aerkeh-9847tdfkzhg4"},
            "device_id": {"description": "710b52d6-9d8f-11e5-9aac-af957c6aaf43"},
            "account_id": {"description": 1},
            "paid_at": {"description": "2011-12-24T16:20:20Z"},
            "sales_date": {"description": "2011-12-25"},
            "price": {"description": "385.0"},
            "change": {"description": "4000.0"},
            "status": {"description": "close"},
            "customers_count": {"description": 0},
            "payments": {"description": "[ $Payments]"},
            "taxes": {"description": "[ $CheckoutTaxes]"},
            "items": {"description": "[ $CheckoutItems]"},
            "customer_tag_ids": {"description": "[10, 1003]"},
            "calculation_option": {"description": ""}
        }


class CheckoutCreate(CheckoutBase):
    """
    Checkout create schema
    """
    ...


class CheckoutPartialUpdate(CheckoutBase):
    """
    Checkout update schema
    """
    ...


class Checkout(CheckoutBase):
    """
    Checkout schema, database representation
    """
    id: int

    class Config:
        fields = {
            "id": {"description": "Unique ID of the checkout"},
        }


class Account(BaseModel):
    ...
