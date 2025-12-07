from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "baza_main.db"

DATA = [
    ("ref_BudgetPart", "PartCode", "02",
        {"PartCode": "02", "ParentPartCode": None, "Name": "Inna Część Budżetu", "IsGroup": 0}),
    ("ref_Dzial", "DzialCode", "102",
        {"DzialCode": "102", "Name": "Inny dział"}),
    ("ref_Rozdzial", "RozdzialCode", "1020",
        {"RozdzialCode": "1020", "DzialId": {"ref": ("ref_Dzial", "DzialCode", "102")}, "Name": "Inny rozdział"}),
    ("ref_Paragraf", "ParagrafCode", "200",
        {"ParagrafCode": "200", "Name": "Materiały i wyposażenie"}),
    ("ref_SourceOfFunding", "SourceCode", "2",
        {"SourceCode": "2", "Name": "Dotacje zewnętrzne"}),
    ("ref_ExpenseGroup", "Name", "Materiały",
        {"Name": "Materiały"}),
    ("ref_BudgetTask", "FullCode", "07.01.02.05",
        {"FullCode": "07.01.02.05", "FunctionNo": "07", "TaskNo": "01", "Description": "Nowe zadanie"}),
    ("org_OrganizationalUnit", "Code", "HR",
        {"Code": "HR", "Name": "Dział Kadr"}),
    ("dim_Dysponent", "Name", "Kierownik HR",
        {"Name": "Kierownik HR", "Notes": "Osoba odpowiedzialna"}),
    ("dbo_BudgetLine", None, None,
        {
            "BudgetPartId": {"ref": ("ref_BudgetPart", "PartCode", "02")},
            "DzialId": {"ref": ("ref_Dzial", "DzialCode", "102")},
            "RozdzialId": {"ref": ("ref_Rozdzial", "RozdzialCode", "1020")},
            "ParagrafId": {"ref": ("ref_Paragraf", "ParagrafCode", "200")},
            "SourceId": {"ref": ("ref_SourceOfFunding", "SourceCode", "2")},
            "ExpenseGroupId": {"ref": ("ref_ExpenseGroup", "Name", "Materiały")},
            "BudgetTaskId": {"ref": ("ref_BudgetTask", "FullCode", "07.01.02.05")},
            "OrgUnitId": {"ref": ("org_OrganizationalUnit", "Code", "HR")},
            "DysponentId": {"ref": ("dim_Dysponent", "Name", "Kierownik HR")},
            "Amount": 2500
        }),
]

def get_id(cur, table, col, val):
    if not col:
        return None
    cur.execute(f"SELECT * FROM {table} WHERE {col}=? LIMIT 1", (val,))
    row = cur.fetchone()
    if not row:
        return None
    cur.execute(f"PRAGMA table_info({table})")
    id_col = cur.fetchone()[1]
    cur.execute(f"SELECT {id_col} FROM {table} WHERE {col}=?", (val,))
    return cur.fetchone()[0]

def resolve(cur, row):
    out, ok = {}, True
    for k, v in row.items():
        if isinstance(v, dict) and "ref" in v:
            ref_id = get_id(cur, *v["ref"])
            if ref_id is None:
                ok = False
            out[k] = ref_id
        else:
            out[k] = v
    return out, ok

def insert(cur, table, data):
    cols = ", ".join(data)
    ph = ", ".join("?" for _ in data)
    cur.execute(f"INSERT OR IGNORE INTO {table} ({cols}) VALUES ({ph})", tuple(data.values()))

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    pending = DATA.copy()

    while pending:
        done = False
        for entry in pending[:]:
            table, ucol, uval, data = entry
            resolved, ok = resolve(cur, data)
            if not ok:
                continue
            insert(cur, table, resolved)
            if ucol:
                print(f"OK: {table} {uval} -> id={get_id(cur, table, ucol, uval)}")
            else:
                print(f"OK: {table} inserted")
            pending.remove(entry)
            done = True

        if not done:
            raise RuntimeError("Nie można rozwiązać zależności FK")

    conn.commit()
    conn.close()
    print("\nWszystko gotowe!")

if __name__ == "__main__":
    main()
