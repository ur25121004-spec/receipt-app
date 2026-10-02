from fastapi import FastAPI
import sqlite3

app = FastAPI()


# データベースを作る
def create_database():
    conn = sqlite3.connect("receipt.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            price INTEGER,
            category TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


# レシートを登録
@app.post("/receipt")
def add_receipt(
    item: str,
    price: int,
    category: str
):
    conn = sqlite3.connect("receipt.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO receipts (item, price, category)
        VALUES (?, ?, ?)
        """,
        (item, price, category)
    )

    conn.commit()
    conn.close()

    return {
        "message": "レシートを登録しました！",
        "商品名": item,
        "金額": price,
        "カテゴリ": category
    }


# レシート一覧を取得
@app.get("/receipts")
def get_receipts():
    conn = sqlite3.connect("receipt.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, item, price, category
        FROM receipts
    """)

    rows = cursor.fetchall()
    conn.close()

    receipts = []

    for row in rows:
        receipts.append({
            "id": row[0],
            "商品名": row[1],
            "金額": row[2],
            "カテゴリ": row[3]
        })

    return receipts