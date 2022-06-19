from tabnanny import check
import unittest

from orm import CheckoutManager

class TestCheckoutManager(unittest.TestCase):
    def test_get_all(self):
        db = CheckoutManager()
        checkouts = db.get_all()

        self.assertEqual(len(checkouts), 3)
        

    def test_get(self):
        db = CheckoutManager()
        checkouts = db.get(2)

        self.assertEqual(checkouts.id, 2)


    def test_update_checkout(self):
        pass
