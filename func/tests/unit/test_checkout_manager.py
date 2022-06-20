from datetime import datetime
from tabnanny import check
import unittest
from ubiapi_manager.checkout import CheckoutManager, SearchCriteria, UbiClientForTest
import schemas
from os.path import dirname as d
from os.path import abspath, join
import json

class TestCheckoutManager(unittest.TestCase):
    def setUp(self) -> None: 
        client = UbiClientForTest(self.get_resp_checkouts())
        self.api_manager = CheckoutManager(client)

    def test_search_all(self):
        checkouts = self.api_manager.search()
        self.assertEqual(len(checkouts), 2)

    def test_search_since(self):
        checkouts = self.api_manager.search(SearchCriteria(since=datetime(2022, 6, 20)))
        self.assertEqual(len(checkouts), 1)

    def test_add(self):
        checkout = schemas.Checkout.parse_obj(self.get_resp_checkouts()["checkouts"][0])
        checkout.guid = "new_guid"

        inserted = self.api_manager.add(checkout)

        self.assertEqual("new_guid", inserted.guid)
        self.assertEqual(len(self.api_manager.search()), 3)

    def get_resp_checkouts(self):
        json_path = "{}\{}".format( d(abspath(__file__)), "resp_checkouts.json")
        with open(json_path, 'r') as json_file:
            json_obj = json.load(json_file)
        return json_obj

    def test_get(self):
        checkout = self.api_manager.get(284886684)
        self.assertEqual(checkout.id, 284886684)

    def test_update_checkout(self):
        pass
