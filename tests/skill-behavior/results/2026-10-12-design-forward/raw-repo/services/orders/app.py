import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("orders.db")

def list_orders(connection):
    rows = connection.execute("SELECT id, status FROM orders ORDER BY id").fetchall()
    return [{"id": row[0], "status": row[1]} for row in rows]

def create_order(connection, order_id):
    connection.execute("INSERT INTO orders(id, status) VALUES (?, ?)", (order_id, "pending"))
    connection.commit()
    return {"id": order_id, "status": "pending"}

# HTTP adapter routes GET /orders -> list_orders and POST /orders -> create_order.
