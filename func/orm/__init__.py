from abc import ABC, abstractmethod
from typing import Optional, List

import schemas


class DatabaseManagerBase(ABC):
    """
    Example implementation of a database manager.
    In a productive application, SQLAlchemy or another ORM framework could be used here (depending on the database used). 
    This is a very simplified database manager for demonstration purposes.
    """

    @abstractmethod
    def add_checkout(self, checkout: schemas.CheckoutCreate) -> schemas.Checkout:
        """
        Adds a checkout to the database
        Args:
            checkout (schemas.CheckoutCreate): Checkout to be added

        Returns:
            schemas.Checkout: Inserted checkout
        """
        ...

    @abstractmethod
    def get_checkouts(self) -> Optional[List[schemas.Checkout]]:
        """
        Returns all checkouts from the database
        Returns:
            Optional[List[schemas.Checkout]]: List of checkouts
        """
        ...

    @abstractmethod
    def get_checkout(self, id: int) -> Optional[schemas.Checkout]:
        """
        Returns a specific checkout by id
        Args:
            id (int): Id of the checkout

        Returns:
            Optional[schemas.Checkout]: Returns the specified checkout
        """
        ...

    @abstractmethod
    def update_checkout(self, checkout_id: int, checkout: schemas.CheckoutPartialUpdate) -> schemas.Checkout:
        """
        Updates a checkout
        Args:
            checkout_id (int): Checkout ID of the checkout to be updated
            checkout (schemas.Checkout): Checkout to update

        Returns:
            schemas.Checkout: Updated checkout
        """
        ...

    @abstractmethod
    def delete_checkout(self, checkout_id: int) -> None:
        """
        Deletes a checkout by id
        Args:
            id (int): Id of the to be deleted checkout
        """
        ...


class FakeDataBaseManager(DatabaseManagerBase):

    def __init__(self) -> None:
        super().__init__()

        self._checkouts = [
            schemas.Checkout(
                id=1,
                title="Checkout 1",
                description="Desc 1",
                purch_price=10,
                sales_price=20
            ),
            schemas.Checkout(
                id=2,
                title="Checkout 2",
                description="Desc 2",
                purch_price=20,
                sales_price=30
            ),
            schemas.Checkout(
                id=3,
                title="Checkout 3",
                description="Desc 3",
                purch_price=40,
                sales_price=65
            )
        ]

    def add_checkout(self, checkout: schemas.CheckoutCreate) -> schemas.Checkout:
        # Normally, this step would be handled by the database
        idx = max([p.id for p in self._checkouts]) + 1

        checkout_insert = schemas.Checkout(id=idx, **checkout.dict())
        self._checkouts.append(checkout_insert)

        return checkout_insert

    def get_checkouts(self) -> Optional[List[schemas.Checkout]]:
        return self._checkouts

    def get_checkout(self, id: int) -> Optional[schemas.Checkout]:
        return next(iter([p for p in self._checkouts if p.id == id]), None)

    def update_checkout(self, checkout_id: int, checkout: schemas.CheckoutPartialUpdate) -> schemas.Checkout:
        for idx, p in enumerate(self._checkouts):
            if p.id == checkout_id:
                db_checkout = self._checkouts[idx]
                update_data = checkout.dict(exclude_unset=True)
                updated_checkout = db_checkout.copy(update=update_data)
                self._checkouts[idx] = updated_checkout
                return updated_checkout
        return None
    
    def delete_checkout(self, checkout_id: int) -> None:
        for p in self._checkouts:
            if p.id == checkout_id:
                checkout_del = p
                break
        
        if checkout_del:
            self._checkouts.remove(checkout_del)
