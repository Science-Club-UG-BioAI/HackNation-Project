import sqlite3
import pandas as pd
import openpyxl
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # folder wyżej
FILE_PATH = BASE_DIR / "db"/"baza_main.db"


conn = sqlite3.connect(FILE_PATH) 
cursor = conn.cursor()


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tabele w bazie:", tables)

nazwa = "dbo_BudgetLine"

cursor.execute(f"SELECT * FROM {nazwa};")
rows = cursor.fetchall()

print(f"\nZawartość tabeli: {nazwa}")
for row in rows:
    print(row)

conn.close()




df = pd.read_sql_query("SELECT * FROM dbo_BudgetLine;", conn)
# print(df.head())

conn.close()