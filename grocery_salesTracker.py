import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME")
)
cursor = conn.cursor()

query = """SELECT p.name AS product_name,p.price,s.quantity,s.date,
(p.price * s.quantity) AS total_amount FROM sales s JOIN  products p ON s.product_id = p.id;"""

df = pd.read_sql(query, conn)

print("\n --- SALES DATA ---\n")
print(df)

total_sales = df["total_amount"].sum()
print(f"\n Total Revenue : RS {total_sales}")

top_item = df.groupby("product_name")["quantity"].sum().sort_values(ascending=False).head(1)
print(f"\n Top selling item (by quantity): ")
print(top_item)

daily_summary = df.groupby("date")['total_amount'].sum()
print("\n Date-wise Revenue : ")
print(daily_summary)

df.to_excel("daily_sales_report.xlsx",index=False)

print("\nReport saved as : daily_sales_report.xlsx")

conn.close() 