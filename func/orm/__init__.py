from abc import ABC, abstractmethod
from typing import Optional, List
import schemas

class CheckoutManager:

    def __init__(self) -> None:
        super().__init__()

        self._checkouts = [
            schemas.Checkout(
                id=1,
                guid= "8928309238-d987aerkeh-9847tdfkzhg4",
                device_id= "710b52d6-9d8f-11e5-9aac-af957c6aaf43",
                account_id= 1,
                paid_at= "2011-12-24T16:20:20Z",
                sales_date= "2011-12-25",
                price= "385.0",
                change= "4000.0",
                status= "close",
                customers_count= 0,
                payments=[ 1, 2, 3],
                taxes = [ 1, 2, 3],
                items= [1, 2, 3],
                customer_tag_ids=[10, 1003],
                calculation_option = schemas.CalculationOption(tax_rounding_mode="down", price_rounding_mode= "plain", tax_calculation_level= "checkout")

            ),
            schemas.Checkout(
                id=2,
                guid= "8928309238-d987aerkeh-9847tdfkzhg5",
                device_id= "710b52d6-9d8f-11e5-9aac-af957c6aaf44",
                account_id= 1,
                paid_at= "2011-12-25T16:20:20Z",
                sales_date= "2011-12-26",
                price= "386.0",
                change= "4001.0",
                status= "close",
                customers_count= 0,
                payments=[ 1, 2, 3],
                taxes = [ 1, 2, 3],
                items= [1, 2, 3],
                customer_tag_ids=[10, 1003],
                calculation_option = schemas.CalculationOption(tax_rounding_mode="down", price_rounding_mode= "plain", tax_calculation_level= "checkout")
            ),
            schemas.Checkout(
                id=3,
                guid= "8928309238-d987aerkeh-9847tdfkzhg6",
                device_id= "710b52d6-9d8f-11e5-9aac-af957c6aaf45",
                account_id= 1,
                paid_at= "2011-12-26T16:20:20Z",
                sales_date= "2011-12-27",
                price= "387.0",
                change= "4002.0",
                status= "close",
                customers_count= 0,
                payments=[ 1, 2, 3],
                taxes = [ 1, 2, 3],
                items= [1, 2, 3],
                customer_tag_ids=[10, 1003],
                calculation_option = schemas.CalculationOption(tax_rounding_mode="down", price_rounding_mode= "plain", tax_calculation_level= "checkout")
            )
        ]

    def add(self, checkout: schemas.CheckoutCreate) -> schemas.Checkout:
        """
        Adds an element to the database
        Args:
            checkout (schemas.CheckoutCreate): Checkout to be added

        Returns:
            schemas.Checkout: Inserted checkout
        """

        # Normally, this step would be handled by the database
        idx = max([p.id for p in self._checkouts]) + 1

        checkout_insert = schemas.Checkout(id=idx, **checkout.dict())
        self._checkouts.append(checkout_insert)

        return checkout_insert

    def get_all(self) -> Optional[List[schemas.Checkout]]:
        """
        Returns all checkouts from the database
        Returns:
            Optional[List[schemas.Checkout]]: List of checkouts
        """

        return self._checkouts

    def get(self, id: int) -> Optional[schemas.Checkout]:
        """
        Returns a specific checkout by id
        Args:
            id (int): Id of the checkout

        Returns:
            Optional[schemas.Checkout]: Returns the specified checkout
        """
        return next(iter([p for p in self._checkouts if p.id == id]), None)

    def update_checkout(self, checkout_id: int, checkout: schemas.CheckoutPartialUpdate) -> schemas.Checkout:
        """
        Updates a checkout
        Args:
            checkout_id (int): Checkout ID of the checkout to be updated
            checkout (schemas.Checkout): Checkout to update

        Returns:
            schemas.Checkout: Updated checkout
        """

        for idx, p in enumerate(self._checkouts):
            if p.id == checkout_id:
                db_checkout = self._checkouts[idx]
                update_data = checkout.dict(exclude_unset=True)
                updated_checkout = db_checkout.copy(update=update_data)
                self._checkouts[idx] = updated_checkout
                return updated_checkout
        return None
    
    def delete_checkout(self, checkout_id: int) -> None:
        """
        Deletes a checkout by id
        Args:
            id (int): Id of the to be deleted checkout
        """
        for p in self._checkouts:
            if p.id == checkout_id:
                checkout_del = p
                break
        
        if checkout_del:
            self._checkouts.remove(checkout_del)
