import logging
from fastapi import APIRouter, Depends
from typing import Optional, List
from func.ubiapi_manager.checkout import CheckoutManagerBase

from dependencies import get_db
from utilities.exceptions import EntityNotFoundException, ApiException
import schemas

router = APIRouter(
    prefix="/checkouts",
    tags=["checkouts"]
)


@router.post("/", response_model=schemas.Checkout, summary="Creates a checkout")
async def add_checkout(checkout_create: schemas.CheckoutCreate, db: CheckoutManagerBase = Depends(get_db)):
    """
    Create a checkout:
    """
    logging.debug("Checkout: Add checkout")
    checkout = db.add(checkout_create)
    return checkout


@router.get(
    "/",
    response_model=Optional[List[schemas.Checkout]],
    summary="Retrieves all checkouts",
    description="Retrieves all available checkouts from the API")
async def read_checkouts(db: CheckoutManagerBase = Depends(get_db)):
    logging.debug("Checkout: Fetch checkouts")
    checkouts = db.search()
    return checkouts


@router.get(
    "/{checkout_id}",
    response_model=Optional[schemas.Checkout],
    summary="Retrieve a checkout by ID",
    description="Retrieves a specific checkout by ID,if no checkout matches the filter criteria a 404 error is returned")
async def read_checkout(checkout_id: int, db: CheckoutManagerBase = Depends(get_db)):
    logging.debug("Checkout: Fetch checkout by id")
    checkout = db.get(checkout_id)
    if not checkout:
        raise EntityNotFoundException(code="Unable to retrieve checkout",
                                      description=f"Checkout with the id {checkout_id} does not exist")
    return checkout


@router.patch("/{checkout_id}", response_model=schemas.Checkout, summary="Patches a checkout")
async def update_checkout(checkout_id: int, checkout_update: schemas.CheckoutPartialUpdate,
                          db: CheckoutManagerBase = Depends(get_db)):
    """ 
    this endpoint allows to update single or multiple values of a checkout
    """
    logging.debug("Checkout: Update checkout")

    if len(checkout_update.dict(exclude_unset=True).keys()) == 0:
        raise ApiException(status_code=400, code="Invalid request",
                           description="Please specify at least one property!")

    checkout = db.update_checkout(checkout_id, checkout_update)
    if not checkout:
        raise EntityNotFoundException(
            code="Unable to update checkout", description=f"Checkout with the id {checkout_id} does not exist")
    return checkout


@router.delete("/{checkout_id}", summary="Deletes a checkout", description="Deletes a checkout permanently by ID")
async def delete_checkout(checkout_id: int, db: CheckoutManagerBase = Depends(get_db)):
    logging.debug("Checkout: Delete checkout")
    db.delete_checkout(checkout_id)
