import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from datetime import datetime


# 保存するCSVファイル
FILE_NAME = "receipt_data.csv"


# =========================
# CSVに保存する
# =========================
def save_data():
    with open(FILE_NAME, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        # 見出し
        writer.writerow(["日付", "商品名", "金額", "カテゴリ"])

        # 表にあるデータを保存
        for item in tree.get_children():
            data = tree.item(item)["values"]
            writer.writerow(data)


# =========================
# CSVから読み込む
# =========================
def load_data():
    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            tree.insert(
                "",
                "end",
                values=(
                    row["日付"],
                    row["商品名"],
                    row["金額"],
                    row["カテゴリ"]
                )
            )

    update_total()


# =========================
# データを登録する
# =========================
def add_data():

    date = date_entry.get()
    item = item_entry.get()
    price = price_entry.get()
    category = category_box.get()

    # 入力チェック
    if date == "" or item == "" or price == "" or category == "":
        messagebox.showwarning(
            "入力エラー",
            "すべての項目を入力してください。"
        )
        return

    # 金額が数字か確認
    try:
        price = int(price)
    except ValueError:
        messagebox.showwarning(
            "入力エラー",
            "金額は数字で入力してください。"
        )
        return

    # データを表に追加
    tree.insert(
        "",
        "end",
        values=(date, item, price, category)
    )

    # 入力欄を空にする
    item_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

    # 合計金額を更新
    update_total()

    # CSVに保存
    save_data()

    messagebox.showinfo(
        "登録完了",
        "レシート情報を登録しました。"
    )


# =========================
# データを削除する
# =========================
def delete_data():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "削除エラー",
            "削除するデータを選択してください。"
        )
        return

    for item in selected:
        tree.delete(item)

    update_total()
    save_data()


# =========================
# 合計金額を計算する
# =========================
def update_total():

    total = 0

    for item in tree.get_children():
        data = tree.item(item)["values"]

        # 金額
        price = int(data[2])

        total += price

    total_label.config(
        text=f"合計金額：{total:,} 円"
    )


# =========================
# カテゴリごとの合計
# =========================
def show_category_total():

    category_total = {}

    for item in tree.get_children():

        data = tree.item(item)["values"]

        price = int(data[2])
        category = data[3]

        if category not in category_total:
            category_total[category] = 0

        category_total[category] += price

    # 結果を表示
    result = ""

    for category, total in category_total.items():
        result += f"{category}：{total:,} 円\n"

    if result == "":
        result = "まだデータがありません。"

    messagebox.showinfo(
        "カテゴリ別合計",
        result
    )


# =========================
# 今日の日付を入れる
# =========================
def set_today():

    today = datetime.now().strftime("%Y/%m/%d")

    date_entry.delete(0, tk.END)
    date_entry.insert(0, today)


# =========================
# メイン画面
# =========================

root = tk.Tk()

root.title("レシート仕分け勘定アプリ")
root.geometry("900x600")


# =========================
# タイトル
# =========================

title_label = tk.Label(
    root,
    text="レシート仕分け勘定アプリ",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=15)


# =========================
# 入力部分
# =========================

input_frame = tk.Frame(root)

input_frame.pack(pady=10)


# 日付
tk.Label(
    input_frame,
    text="購入日"
).grid(row=0, column=0, padx=5, pady=5)

date_entry = tk.Entry(
    input_frame,
    width=15
)

date_entry.grid(row=0, column=1, padx=5)

set_today()


# 商品名
tk.Label(
    input_frame,
    text="商品名"
).grid(row=0, column=2, padx=5)

item_entry = tk.Entry(
    input_frame,
    width=20
)

item_entry.grid(row=0, column=3, padx=5)


# 金額
tk.Label(
    input_frame,
    text="金額"
).grid(row=1, column=0, padx=5, pady=5)

price_entry = tk.Entry(
    input_frame,
    width=15
)

price_entry.grid(row=1, column=1, padx=5)


# カテゴリ
tk.Label(
    input_frame,
    text="カテゴリ"
).grid(row=1, column=2, padx=5)

category_box = ttk.Combobox(
    input_frame,
    values=[
        "食品",
        "日用品",
        "必需品",
        "車用品",
        "その他"
    ],
    width=17,
    state="readonly"
)

category_box.grid(row=1, column=3, padx=5)

category_box.set("食品")


# =========================
# 登録ボタン
# =========================

add_button = tk.Button(
    root,
    text="レシートを登録",
    command=add_data,
    width=20,
    height=2
)

add_button.pack(pady=10)


# =========================
# データ一覧
# =========================

columns = (
    "date",
    "item",
    "price",
    "category"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=12
)

tree.heading(
    "date",
    text="購入日"
)

tree.heading(
    "item",
    text="商品名"
)

tree.heading(
    "price",
    text="金額"
)

tree.heading(
    "category",
    text="カテゴリ"
)


tree.column(
    "date",
    width=150
)

tree.column(
    "item",
    width=250
)

tree.column(
    "price",
    width=150
)

tree.column(
    "category",
    width=150
)


tree.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)


# =========================
# ボタン
# =========================

button_frame = tk.Frame(root)

button_frame.pack(pady=10)


delete_button = tk.Button(
    button_frame,
    text="選択したデータを削除",
    command=delete_data
)

delete_button.grid(
    row=0,
    column=0,
    padx=10
)


category_button = tk.Button(
    button_frame,
    text="カテゴリ別集計",
    command=show_category_total
)

category_button.grid(
    row=0,
    column=1,
    padx=10
)


# =========================
# 合計金額
# =========================

total_label = tk.Label(
    root,
    text="合計金額：0 円",
    font=("Arial", 18, "bold")
)

total_label.pack(pady=10)


# =========================
# 保存データを読み込む
# =========================

load_data()


# =========================
# アプリ開始
# =========================

root.mainloop()