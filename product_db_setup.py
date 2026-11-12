import sqlite3

def get_db():
    conn = sqlite3.connect("product.db")
    conn.row_factory = sqlite3.Row
    return conn

with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS product(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT UNIQUE NOT NULL,
            price INT NOT NULL
        )
    """)

products_list = [

    ("Bread", 25),

    ("Milk", 35),

    ("Cheese", 28)

]

with sqlite3.connect("product.db") as conn:
    cursor = conn.cursor()

    sql = "INSERT INTO product (product_name, price) VALUES (?, ?)"

    cursor.executemany(sql, products_list)

    conn.commit()