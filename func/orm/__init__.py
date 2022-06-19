from abc import ABC, abstractmethod
from typing import Optional, List
import schemas

class CheckoutManagerBase(ABC):
    @abstractmethod
    def add(self, checkout: schemas.CheckoutCreate) -> schemas.Checkout:
        """
        Adds a checkout to the database
        Args:
            checkout (schemas.CheckoutCreate): Checkout to be added

        Returns:
            schemas.Checkout: Inserted checkout
        """
        ...

    @abstractmethod
    def search(self) -> Optional[List[schemas.Checkout]]:
        """
        Returns checkouts under some criteria
        Returns:
            Optional[List[schemas.Checkout]]: List of checkouts
        """
        ...

    @abstractmethod
    def get(self, id: int) -> Optional[schemas.Checkout]:
        """
        Returns a checkout from the database
        Args:
            id (int): Checkout ID of the checkout to be updated
        Returns:
            Optional[schemas.Checkout]: Checkout
        """
        ...

    @abstractmethod
    def update(self, id: int, checkout: schemas.CheckoutPartialUpdate) -> schemas.Checkout:
        """
        Updates a checkout
        Args:
            id (int): Checkout ID of the checkout to be updated
            checkout (schemas.Checkout): Checkout to update

        Returns:
            schemas.Checkout: Updated checkout
        """
        ...

    @abstractmethod
    def delete(self, id: int) -> None:
        """
        Deletes a checkout by id
        Args:
            id (int): Id of the to be deleted checkout
        """
        ...

class CheckoutManager:

    def __init__(self, checkouts : Optional[List[schemas.Checkout]]= []) -> None:
        super().__init__()
        self._checkouts = checkouts

    def add(self, checkout: schemas.CheckoutCreate) -> schemas.Checkout:
        # Normally, this step would be handled by the database
        idx = max([p.id for p in self._checkouts]) + 1

        checkout_insert = schemas.Checkout(id=idx, **checkout.dict())
        self._checkouts.append(checkout_insert)

        return checkout_insert

    def search(self) -> Optional[List[schemas.Checkout]]:
        return self._checkouts

    def get(self, id: int) -> Optional[schemas.Checkout]:
        return next(iter([p for p in self._checkouts if p.id == id]), None)

    def update(self, id: int, checkout: schemas.CheckoutPartialUpdate) -> schemas.Checkout:
        for idx, p in enumerate(self._checkouts):
            if p.id == id:
                db_checkout = self._checkouts[idx]
                update_data = checkout.dict(exclude_unset=True)
                updated_checkout = db_checkout.copy(update=update_data)
                self._checkouts[idx] = updated_checkout
                return updated_checkout
        return None
    
    def delete(self, id: int) -> None:
        for p in self._checkouts:
            if p.id == id:
                checkout_del = p
                break
        
        if checkout_del:
            self._checkouts.remove(checkout_del)
