import sqlite3
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("orders", ROOT / "services/orders/app.py")
orders = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orders)

class OrdersTest(unittest.TestCase):
    def test_create_and_list(self):
        connection = sqlite3.connect(":memory:")
        connection.executescript((ROOT / "services/orders/schema.sql").read_text())
        self.assertEqual(orders.create_order(connection, 1), {"id": 1, "status": "pending"})
        self.assertEqual(orders.list_orders(connection), [{"id": 1, "status": "pending"}])
    def test_empty(self):
        connection = sqlite3.connect(":memory:")
        connection.executescript((ROOT / "services/orders/schema.sql").read_text())
        self.assertEqual(orders.list_orders(connection), [])
