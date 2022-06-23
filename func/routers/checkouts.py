from fastapi import APIRouter, Depends
from typing import Optional, List

from utilities.utils import get_logger
from dependencies import get_checkout_man
from utilities.exceptions import EntityNotFoundException, ApiException
import ubiclient

logger = get_logger(__name__)

router = APIRouter(
    prefix="/checkouts",
    tags=["checkouts"]
)


@router.post("/", response_model=ubiclient.Checkout, summary="Creates a checkout")
async def add_checkout(checkout_create: ubiclient.CheckoutCreate, client: ubiclient.CheckoutManagerBase = Depends(get_checkout_man)):
    """
    Create a checkout:
    """
    logger.debug("Checkout: Add checkout")
    checkout = client.add(checkout_create)
    return checkout


@router.get(
    "/",
    response_model=Optional[List[ubiclient.Checkout]],
    summary="Retrieves all checkouts",
    description="Retrieves all available checkouts from the API")
async def read_checkouts(client: ubiclient.CheckoutManagerBase = Depends(get_checkout_man)):
    logger.debug("Checkout: Fetch checkouts")
    checkouts = client.search()
    return checkouts


@router.get(
    "/{checkout_id}",
    response_model=Optional[ubiclient.Checkout],
    summary="Retrieve a checkout by ID",
    description="Retrieves a specific checkout by ID,if no checkout matches the filter criteria a 404 error is returned")
async def read_checkout(checkout_id: int, client: ubiclient.CheckoutManagerBase = Depends(get_checkout_man)):
    logger.debug("Checkout: Fetch checkout by id")
    checkout = client.get(checkout_id)
    if not checkout:
        raise EntityNotFoundException(code="Unable to retrieve checkout",
                                      description=f"Checkout with the id {checkout_id} does not exist")
    return checkout


@router.patch("/{checkout_id}", response_model=ubiclient.Checkout, summary="Patches a checkout")
async def update_checkout(checkout_id: int, checkout_update: ubiclient.CheckoutPartialUpdate,
                          client: ubiclient.CheckoutManagerBase = Depends(get_checkout_man)):
    """ 
    this endpoint allows to update single or multiple values of a checkout
    """
    logger.debug("Checkout: Update checkout")

    if len(checkout_update.dict(exclude_unset=True).keys()) == 0:
        raise ApiException(status_code=400, code="Invalid request",
                           description="Please specify at least one property!")

    checkout = client.update_checkout(checkout_id, checkout_update)
    if not checkout:
        raise EntityNotFoundException(
            code="Unable to update checkout", description=f"Checkout with the id {checkout_id} does not exist")
    return checkout


@router.delete("/{checkout_id}", summary="Deletes a checkout", description="Deletes a checkout permanently by ID")
async def delete_checkout(checkout_id: int, client: ubiclient.CheckoutManagerBase = Depends(get_checkout_man)):
    logger.debug("Checkout: Delete checkout")
    client.delete_checkout(checkout_id)
