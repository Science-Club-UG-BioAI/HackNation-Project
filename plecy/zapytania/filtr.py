#!/usr/bin/env python3


from pathlib import Path
import sqlite3
import sys
from typing import Dict, Optional
from openpyxl import Workbook

# --- ustaw DB_PATH jeśli chcesz inny niż domyślny ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "baza_main.db"

# --- preferowana kolejność tabel ---
PREFERRED_ORDER = [
    "ref_BudgetPart",
    "ref_Dzial",
    "ref_Rozdzial",
    "ref_Paragraf",
    "ref_SourceOfFunding",
    "ref_ExpenseGroup",
    "ref_BudgetTask",
    "org_OrganizationalUnit",
    "dim_Dysponent",
]

# ---------- helpery ----------
def get_table_list(cur):
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
    )
    return [r[0] for r in cur.fetchall()]

def get_columns(cur, table):
    cur.execute(f"PRAGMA table_info({table})")
    # returns list of (cid, name, type, notnull, dflt_value, pk)
    return [row[1] for row in cur.fetchall()]

def choose_id_and_display_column(cols):
    # prefer an Id column (endswith 'Id') and a display column (Name, Code, FullCode)
    id_col = None
    display_col = None
    for c in cols:
        if c.lower().endswith("id") and id_col is None:
            id_col = c
    # display preferences
    for prefer in ("Name", "Code", "FullCode", "DzialCode", "PartCode", "ParagrafCode"):
        if prefer in cols:
            display_col = prefer
            break
    if display_col is None:
        # choose first column that is not id_col
        for c in cols:
            if c != id_col:
                display_col = c
                break
    return id_col, display_col

def get_distinct_values(cur, table, id_col, display_col, limit=200):
    q = f"SELECT {id_col}, {display_col} FROM {table} GROUP BY {id_col}, {display_col} ORDER BY {display_col} LIMIT {limit}"
    cur.execute(q)
    return cur.fetchall()

def save_to_excel(filename: str, colnames, rows):
    """
    Save results to an .xlsx file using openpyxl.
    Converts None to empty string for nicer Excel output.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    # zapisz nagłówki
    ws.append(list(colnames))

    # zapisz wiersze, zamieniając None -> ""
    for row in rows:
        ws.append([x if x is not None else "" for x in row])

    wb.save(filename)
    print(f"Zapisano wynik do pliku: {filename}")

# ------------ build/join/query ------------
def build_query_and_params(tables_meta, selected_filters: Dict[str, Optional[int]]):
    select_cols = ["b.BudgetLineId", "b.Amount"]
    joins = []
    where_clauses = []
    params = []

    # We'll create aliases t1, t2...
    alias_i = 1
    # tables_meta is an ordered dict-like mapping: iteration order determines JOIN order
    for table, meta in tables_meta.items():
        id_col, display_col, fk_in_budgetline = meta
        if fk_in_budgetline is None:
            # table not referenced by dbo_BudgetLine directly — we can still left join on possible relation by guessing
            fk_in_budgetline = f"{table.split('_')[-1].capitalize()}Id"  # fallback guess
        alias = f"t{alias_i}"
        alias_i += 1
        # join only if id_col exists
        joins.append(f"LEFT JOIN {table} {alias} ON {alias}.{id_col} = b.{fk_in_budgetline}")
        select_cols.append(f"{alias}.{display_col} AS {table}_{display_col}")
        # if user selected filter on this table, add WHERE
        chosen = selected_filters.get(table)
        if chosen is not None:
            where_clauses.append(f"{alias}.{id_col} = ?")
            params.append(chosen)
    select_sql = ", ".join(select_cols)
    join_sql = "\n".join(joins)
    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    sql = f"""
    SELECT {select_sql}
    FROM dbo_BudgetLine b
    {join_sql}
    {where_sql}
    ORDER BY b.BudgetLineId
    """
    return sql, params

# ------------ main interactive function ------------
def interactive_run(db_path: Path):
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    tables = get_table_list(cur)
    # we treat dbo_BudgetLine specially: it's the 'fact' table we return rows from.
    if "dbo_BudgetLine" not in tables:
        print("Błąd: nie znaleziono tabeli dbo_BudgetLine w bazie.")
        return
    # use preferred order but only keep existing tables
    filter_tables = [t for t in PREFERRED_ORDER if t in tables]

    # gather metadata (id/display col and guess fk column name in dbo_BudgetLine)
    tables_meta = {}
    for t in filter_tables:
        cols = get_columns(cur, t)
        if not cols:
            continue
        id_col, display_col = choose_id_and_display_column(cols)
        # guess how dbo_BudgetLine stores FK to this table: try common patterns
        # pattern: table name parts -> last part + 'Id' e.g. ref_BudgetPart -> BudgetPartId
        last_part = t.split("_")[-1]
        possible_fk = f"{last_part}Id"
        # fallback list of known names in your schema
        known_fks = {
            "ref_BudgetPart": "BudgetPartId",
            "ref_Dzial": "DzialId",
            "ref_Rozdzial": "RozdzialId",
            "ref_Paragraf": "ParagrafId",
            "ref_SourceOfFunding": "SourceId",
            "ref_ExpenseGroup": "ExpenseGroupId",
            "ref_BudgetTask": "BudgetTaskId",
            "org_OrganizationalUnit": "OrgUnitId",
            "dim_Dysponent": "DysponentId",
        }
        fk_in_budgetline = known_fks.get(t, possible_fk)
        tables_meta[t] = (id_col, display_col, fk_in_budgetline)

    print("Znalezione tabele do filtrowania (kolejność):")
    for i, t in enumerate(filter_tables, 1):
        id_col, display_col, fk = tables_meta.get(t, (None, None, None))
        print(f"{i}. {t}  (id: {id_col}, display: {display_col}, fk w dbo_BudgetLine: {fk})")
    print("\nDla każdej tabeli możesz wybrać wartość filtrującą lub wpisać 0 aby pominąć.")

    selected_filters: Dict[str, Optional[int]] = {}
    for t in filter_tables:
        id_col, display_col, fk = tables_meta.get(t, (None, None, None))
        if id_col is None or display_col is None:
            print(f"\nTabela: {t}  — brak kolumn do użycia, pomijam.")
            selected_filters[t] = None
            continue
        print(f"\nTabela: {t}  — kolumna do wyświetlenia: {display_col}")
        rows = get_distinct_values(cur, t, id_col, display_col, limit=500)
        if not rows:
            print("  (brak wartości w tabeli — pomijam)")
            selected_filters[t] = None
            continue
        print("  Wybierz jedną z poniższych wartości (numer). 0 = pomiń (nie filtrować):")
        # print enumerated list
        for idx, (iid, disp) in enumerate(rows, start=1):
            print(f"   {idx}. {disp} (id={iid})")
        # get input
        while True:
            ans = input(f"Twój wybór dla {t} [0-{len(rows)}]: ").strip()
            if ans == "":
                ans = "0"
            if not ans.isdigit():
                print("  Proszę wpisać numer.")
                continue
            n = int(ans)
            if 0 <= n <= len(rows):
                break
            print("  Nieprawidłowy numer.")
        if n == 0:
            selected_filters[t] = None
        else:
            chosen_id = rows[n - 1][0]
            selected_filters[t] = chosen_id
            print(f"  Wybrano id={chosen_id} ({rows[n-1][1]})")

    # build query
    sql, params = build_query_and_params(tables_meta, selected_filters)
    print("\n--- Wykonuję zapytanie ---")
    # print(sql)   # odkomentuj jeśli chcesz zobaczyć zapytanie
    cur.execute(sql, params)
    colnames = [d[0] for d in cur.description]
    results = cur.fetchall()
    if not results:
        print("Brak wierszy spełniających filtry.")
    else:
        # print header
        print("\t".join(colnames))
        for row in results:
            print("\t".join(str(x) if x is not None else "" for x in row))

        # zapis do Excela (interactive)
        save_to_excel("wynik.xlsx", colnames, results)

    conn.close()

# ------------ programmatic run ------------
def programmatic_run(db_path: Path, filters: Dict[str, Optional[int]]):
    """
    filters: mapping table_name -> id to filter on (or None to skip)
    Example:
       {"ref_BudgetPart": 1, "ref_Dzial": None, "dim_Dysponent": 1}
    """
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    tables = get_table_list(cur)
    # use preferred order but only include tables that exist
    filter_tables = [t for t in PREFERRED_ORDER if t in tables]

    tables_meta = {}
    for t in filter_tables:
        cols = get_columns(cur, t)
        if not cols:
            continue
        id_col, display_col = choose_id_and_display_column(cols)
        known_fks = {
            "ref_BudgetPart": "BudgetPartId",
            "ref_Dzial": "DzialId",
            "ref_Rozdzial": "RozdzialId",
            "ref_Paragraf": "ParagrafId",
            "ref_SourceOfFunding": "SourceId",
            "ref_ExpenseGroup": "ExpenseGroupId",
            "ref_BudgetTask": "BudgetTaskId",
            "org_OrganizationalUnit": "OrgUnitId",
            "dim_Dysponent": "DysponentId",
        }
        fk_in_budgetline = known_fks.get(t, f"{t.split('_')[-1].capitalize()}Id")
        tables_meta[t] = (id_col, display_col, fk_in_budgetline)

    # ensure all keys exist in filters (missing -> None)
    selected_filters = {t: filters.get(t) if t in filters else None for t in filter_tables}
    sql, params = build_query_and_params(tables_meta, selected_filters)
    cur.execute(sql, params)
    colnames = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()
    # return header + rows
    return colnames, rows

# ------------ if run as script ------------
if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"Nie znaleziono bazy danych pod {DB_PATH}. Upewnij się, że ścieżka jest poprawna.")
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == "--programmatic":
        # przykład programowego uruchomienia
        # możesz tu zmienić filtry: klucz = nazwa tabeli, wartość = id z tej tabeli lub None
        example_filters = {
            "ref_BudgetPart": 1,
            "ref_Dzial": None,
            "dim_Dysponent": None,
        }
        cols, rows = programmatic_run(DB_PATH, example_filters)
        if not rows:
            print("Brak wierszy.")
        else:
            print("\t".join(cols))
            for r in rows:
                print("\t".join(str(x) if x is not None else "" for x in r))
            # zapis do Excela (programmatic)
            save_to_excel("wynik_programmatic.xlsx", cols, rows)
    else:
        interactive_run(DB_PATH)
