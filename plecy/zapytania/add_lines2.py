from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "baza_main.db"

# =====================
#  INNE DANE (nowy zestaw)
# =====================
DATA = [
    ("ref_BudgetPart", "PartCode", "03",
        {"PartCode": "03", "ParentPartCode": None, "Name": "Biuro Rzecznika", "IsGroup": 0}),
    ("ref_Dzial", "DzialCode", "103",
        {"DzialCode": "103", "Name": "Edukacja i kultura"}),
    ("ref_Rozdzial", "RozdzialCode", "1030",
        {"RozdzialCode": "1030", "DzialId": {"ref": ("ref_Dzial", "DzialCode", "103")}, "Name": "Wydatki kulturalne"}),
    ("ref_Paragraf", "ParagrafCode", "300",
        {"ParagrafCode": "300", "Name": "Usługi obce"}),
    ("ref_SourceOfFunding", "SourceCode", "3",
        {"SourceCode": "3", "Name": "Środki europejskie"}),
    ("ref_ExpenseGroup", "Name", "Usługi",
        {"Name": "Usługi"}),
    ("ref_BudgetTask", "FullCode", "08.02.03.06",
        {"FullCode": "08.02.03.06", "FunctionNo": "08", "TaskNo": "02", "Description": "Zadanie kulturalne"}),
    ("org_OrganizationalUnit", "Code", "FIN",
        {"Code": "FIN", "Name": "Departament Finansów"}),
    ("dim_Dysponent", "Name", "Kierownik Finansowy",
        {"Name": "Kierownik Finansowy", "Notes": "Odpowiedzialny za wydatki finansowe"}),
    ("dbo_BudgetLine", None, None,
        {
            "BudgetPartId": {"ref": ("ref_BudgetPart", "PartCode", "03")},
            "DzialId": {"ref": ("ref_Dzial", "DzialCode", "103")},
            "RozdzialId": {"ref": ("ref_Rozdzial", "RozdzialCode", "1030")},
            "ParagrafId": {"ref": ("ref_Paragraf", "ParagrafCode", "300")},
            "SourceId": {"ref": ("ref_SourceOfFunding", "SourceCode", "3")},
            "ExpenseGroupId": {"ref": ("ref_ExpenseGroup", "Name", "Usługi")},
            "BudgetTaskId": {"ref": ("ref_BudgetTask", "FullCode", "08.02.03.06")},
            "OrgUnitId": {"ref": ("org_OrganizationalUnit", "Code", "FIN")},
            "DysponentId": {"ref": ("dim_Dysponent", "Name", "Kierownik Finansowy")},
            "Amount": 5000
        }),
]

# =====================
#  LOGIKA (bez zmian)
# =====================
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
            raise RuntimeError("Nie można rozwiązać zależności FK — sprawdź definicje w DATA")

    conn.commit()
    conn.close()
    print("\nWszystko gotowe!")

if __name__ == "__main__":
    main()
