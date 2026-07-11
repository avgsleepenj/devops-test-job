import unittest
from types import SimpleNamespace
from unittest.mock import patch

import app as shelter


class FakeCursor(list):
    def sort(self, *_args, **_kwargs):
        return self


class FakeCollection:
    def __init__(self):
        self.last_query = None

    def find(self, query, _projection):
        self.last_query = query
        return FakeCursor(
            [
                {
                    "name": "Лисса",
                    "age": 4,
                    "breed": "Метис",
                    "photo": "https://example.test/cat.jpg",
                    "status": "ищет дом",
                }
            ]
        )


class FakeAdmin:
    def command(self, name):
        if name != "ping":
            raise AssertionError(f"Unexpected command: {name}")
        return {"ok": 1}


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.collection = FakeCollection()
        self.collection_patch = patch.object(
            shelter, "cats_collection", self.collection
        )
        self.client_patch = patch.object(
            shelter,
            "mongo_client",
            SimpleNamespace(admin=FakeAdmin()),
        )
        self.collection_patch.start()
        self.client_patch.start()
        self.client = shelter.app.test_client()

    def tearDown(self):
        self.collection_patch.stop()
        self.client_patch.stop()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_list_and_filters(self):
        response = self.client.get("/api/cats?name=лис&age=4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["name"], "Лисса")
        self.assertEqual(self.collection.last_query["age"], 4)
        self.assertEqual(self.collection.last_query["name"]["$regex"], "лис")

    def test_invalid_age(self):
        for age in ("abc", "-1", "41"):
            with self.subTest(age=age):
                response = self.client.get(f"/api/cats?age={age}")
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_unknown_route(self):
        response = self.client.get("/missing")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
