print(__name__)
import unittest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from routers.checkouts import router as checkout_router


class TestCheckouts(unittest.TestCase):
    def setUp(self) -> None:
        self.app = FastAPI()
        self.app.include_router(checkout_router)
        self.client = TestClient(self.app)

    def test_bar(self):
        response = self.client.get("/checkouts")
        self.assertEqual(200, response.status_code)
        checkouts = response.json()
        self.assertGreater(len(checkouts), 0)