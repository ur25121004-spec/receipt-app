from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()


# =========================
# データベース
# =========================

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


# =========================
# レシート勘定アプリ画面
# =========================

@app.get("/", response_class=HTMLResponse)
def home():

    conn = sqlite3.connect("receipt.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, item, price, category
        FROM receipts
        ORDER BY id
    """)

    rows = cursor.fetchall()
    conn.close()

    total = sum(row[2] for row in rows)

    category_totals = {}

    for row in rows:
        category = row[3]
        price = row[2]

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += price


    html = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>レシート勘定アプリ</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
            }

            h1 {
                text-align: center;
            }

            .input-area {
                border: 1px solid #ccc;
                padding: 20px;
                margin-bottom: 30px;
            }

            input, select, button {
                padding: 8px;
                margin: 5px;
            }

            button {
                cursor: pointer;
            }

            table {
                width: 100%;
                border-collapse: collapse;
            }

            th, td {
                border: 1px solid #ccc;
                padding: 10px;
                text-align: center;
            }

            th {
                background-color: #f2f2f2;
            }

            .total {
                font-size: 24px;
                font-weight: bold;
                margin: 20px 0;
            }
        </style>
    </head>

    <body>

        <h1>レシート勘定アプリ</h1>

        <div class="input-area">

            <h2>レシートを登録</h2>

            <form action="/receipt" method="post">

                <div>
                    商品名：
                    <input type="text" name="item" required>
                </div>

                <div>
                    金額：
                    <input type="number" name="price" required>
                    円
                </div>

                <div>
                    カテゴリ：
                    <select name="category">
                        <option value="食品">食品</option>
                        <option value="日用品">日用品</option>
                        <option value="必需品">必需品</option>
                        <option value="車用品">車用品</option>
                        <option value="アルコール">アルコール</option>
                        <option value="その他">その他</option>
                    </select>
                </div>

                <button type="submit">
                    レシートを登録
                </button>

            </form>

        </div>

        <div class="total">
            合計金額：""" + f"{total:,}" + """ 円
        </div>
       
            
    <h2>登録したレシート</h2>

    <table>

     <tr>
                <th>ID</th>
                <th>商品名</th>
                <th>金額</th>
                <th>カテゴリ</th>
                <th>操作</th>
            </tr>
    """

    for row in rows:

        html += f"""
            <tr>
               <td>{row[0]}</td>
               <td>{row[1]}</td>
               <td>{row[2]:,} 円</td>
               <td>{row[3]}</td>
               <td>
                   <form action="/receipt/delete/{row[0]}" method="post">
                       <button type="submit">削除</button>
                   </form>
               </td>
            </tr>
    """

    html += """
       </table>

       <h2>カテゴリ別合計</h2>

       <ul>
   """

    for category, amount in category_totals.items():

        html += f"""
            <li>{category}：{amount:,} 円</li>
     """

    html += """
        </ul>

    </body>
    </html>
    """

    return html

# =========================
# レシート登録
# =========================

@app.post("/receipt", response_class=HTMLResponse)
def add_receipt(
    item: str = Form(...),
    price: int = Form(...),
    category: str = Form(...)
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

    return """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>登録完了</title>
    </head>

    <body>
        <h1>レシートを登録しました！</h1>

        <p>商品名：""" + item + """</p>
        <p>金額：""" + str(price) + """ 円</p>
        <p>カテゴリ：""" + category + """</p>

        <a href="/">レシート一覧に戻る</a>
    </body>
    </html>
    """

    return {
        "message": "レシートを登録しました！",
        "商品名": item,
        "金額": price,
        "カテゴリ": category
    }


# =========================
# レシート一覧
# =========================

@app.get("/receipts")
def get_receipts():

    conn = sqlite3.connect("receipt.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, item, price, category
        FROM receipts
        ORDER BY id
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

@app.post("/receipt/delete/{receipt_id}", response_class=HTMLResponse)
def delete_receipt(receipt_id: int):

    conn = sqlite3.connect("receipt.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM receipts WHERE id = ?",
        (receipt_id,)
    )

    conn.commit()
    conn.close()

    return """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>削除完了</title>
    </head>

    <body>
        <h1>レシートを削除しました！</h1>

        <a href="/">レシート一覧に戻る</a>
    </body>
    </html>
    """