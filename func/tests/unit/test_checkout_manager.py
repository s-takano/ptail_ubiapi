from tabnanny import check
import unittest

from orm import CheckoutManager
import schemas

class TestCheckoutManager(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        
        self.checkouts = [
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

    def test_search(self):
        db = CheckoutManager(self.checkouts)
        checkouts = db.search()

        self.assertEqual(len(checkouts), 3)

    def test_get(self):
        db = CheckoutManager(self.checkouts)
        checkouts = db.get(2)

        self.assertEqual(checkouts.id, 2)

    def test_update_checkout(self):
        pass
