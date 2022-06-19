from tabnanny import check
import unittest

from orm import FakeDataBaseManager

class TestUbiWrapper(unittest.TestCase):
    def test_get_checkouts(self):
        db = FakeDataBaseManager()
        checkouts = db.get_checkouts()

        self.assertEqual(len(checkouts), 3)
        

    def test_get_checkout(self):
        db = FakeDataBaseManager()
        checkouts = db.get_checkout(1)

        self.assertEqual(checkouts.id, 1)


    def test_update_checkout(self):
        pass
