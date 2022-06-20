from abc import ABC, abstractmethod
from ast import parse
from datetime import datetime
from msilib import schema
from dateutil import parser
from typing import Optional, List

from pydantic import BaseModel
from schemas import Checkout, Account
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

class SearchCriteria(BaseModel):
    @staticmethod
    def get_default():
        return SearchCriteria(since=datetime(1900, 1, 1))

    def meets(self, checkout : schemas.CheckoutBase):
        return parser.parse(checkout["sales_date"]) >= self.since
        # item | since ≤ item.updated_at ⋀ item.updated_at < until ⋀ glb < item.id

    since : Optional[datetime]
    until : Optional[datetime]
    limit : Optional[datetime]
    glb : Optional[datetime]

class UbiResponse(BaseModel):
    timestamp : datetime # "2022-06-20T08:32:52Z"

class SimpleReponse(UbiResponse):
    account : Optional[Account]
    checkout : Optional[Checkout]

class CollectionReponse(UbiResponse):
    next_batch_since : datetime # "2022-06-19T21:34:21Z"
    last_updated_at  : datetime # "2022-06-19T21:34:20Z"
    next_url : Optional[str] #": null,

    checkouts : Optional[List[Checkout]]

    class Config:
        alias_generator = lambda str : "next-url" if str=="next_url" else str


class UbiClientBase(ABC):
    @abstractmethod
    def add(self, resource) -> SimpleReponse:
        ...

    @abstractmethod
    def search(self, criteria) -> CollectionReponse:
        ...

    @abstractmethod
    def get(self, id) -> SimpleReponse:
        ...

    @abstractmethod
    def update(self, id: int, resource) -> None:
        ...

    @abstractmethod
    def delete(self, id) -> None:
        ...



class UbiClient(UbiClientBase):
    def add(self, resource) -> SimpleReponse:
        ...

    def search(self, criteria) -> CollectionReponse:
        ...

    def get(self, id) -> SimpleReponse:
        ...

    def update(self, id: int, resource) -> None:
        ...

    def delete(self, id) -> None:
        ...



class UbiClientForTest(UbiClientBase):
    def __init__(self, resp_checkouts : dict) -> None:
        self._resp_checkouts = resp_checkouts

    def add(self, resource) -> SimpleReponse:
        idx = max([p["id"] for p in self._resp_checkouts["checkouts"]]) + 1
        resource["id"] = idx
        self._resp_checkouts["checkouts"].append(resource)
        return SimpleReponse(timestamp="2022-06-20T08:32:52Z", checkout=resource)

    def search(self, criteria) -> CollectionReponse:
        copy = self._resp_checkouts.copy()
        copy["checkouts"] = [e for e in copy["checkouts"] if criteria.meets(e) ]
        return CollectionReponse.parse_obj(copy)

    def get(self, id) -> SimpleReponse:
        return SimpleReponse(timestamp="2022-06-20T08:32:52Z", checkout=next(iter([p for p in self._resp_checkouts["checkouts"] if p["id"] == id]), None))

    def update(self, id: int, resource) -> None:
        for idx, p in enumerate(self._resp_checkouts["checkouts"]):
            if p.id == id:
                db_checkout = self._resp_checkouts["checkouts"][idx]
                update_data = resource.dict(exclude_unset=True)
                updated_checkout = db_checkout.copy(update=update_data)
                self._resp_checkouts["checkouts"][idx] = updated_checkout
                return updated_checkout
        return None

    def delete(self, id) -> None:
        for p in self._resp_checkouts:
            if p.id == id:
                checkout_del = p
                break
        
        if checkout_del:
            self._resp_checkouts.remove(checkout_del)


class CheckoutManager(CheckoutManagerBase):

    def __init__(self, client : UbiClientBase) -> None:
        super().__init__()
        self.client = client

    def add(self, checkout: schemas.CheckoutCreate) -> schemas.Checkout:
        resp = self.client.add(checkout.dict())
        return resp.checkout


    def search(self, criteria : Optional[SearchCriteria] = None) -> Optional[List[schemas.Checkout]]:
        if criteria is None:
            criteria = SearchCriteria.get_default()

        resp = self.client.search(criteria)

        return resp.checkouts


    def get(self, id: int) -> Optional[schemas.Checkout]:
        resp = self.client.get(id)
        return schemas.Checkout.parse_obj(resp.checkout)


    def update(self, id: int, checkout: schemas.CheckoutPartialUpdate) -> schemas.Checkout:
        resp = self.client.update(id, checkout.dict())
        return resp
    
    def delete(self, id: int) -> None:
        self.client.delete(id)

