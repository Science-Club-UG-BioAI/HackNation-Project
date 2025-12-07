from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "baza_main.db"

DB_PATH.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON;")

cur.executescript(
    """
CREATE TABLE IF NOT EXISTS ref_BudgetPart (
    BudgetPartId INTEGER PRIMARY KEY AUTOINCREMENT,
    PartCode TEXT NOT NULL UNIQUE,
    ParentPartCode TEXT,
    Name TEXT NOT NULL,
    IsGroup INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS ref_Dzial (
    DzialId INTEGER PRIMARY KEY AUTOINCREMENT,
    DzialCode TEXT NOT NULL UNIQUE,
    Name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ref_Rozdzial (
    RozdzialId INTEGER PRIMARY KEY AUTOINCREMENT,
    RozdzialCode TEXT NOT NULL UNIQUE,
    DzialId INTEGER NOT NULL,
    Name TEXT NOT NULL,
    FOREIGN KEY (DzialId) REFERENCES ref_Dzial(DzialId)
);

CREATE TABLE IF NOT EXISTS ref_Paragraf (
    ParagrafId INTEGER PRIMARY KEY AUTOINCREMENT,
    ParagrafCode TEXT NOT NULL UNIQUE,
    Name TEXT
);

CREATE TABLE IF NOT EXISTS ref_SourceOfFunding (
    SourceId INTEGER PRIMARY KEY AUTOINCREMENT,
    SourceCode TEXT NOT NULL UNIQUE,
    Name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ref_ExpenseGroup (
    ExpenseGroupId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ref_BudgetTask (
    BudgetTaskId INTEGER PRIMARY KEY AUTOINCREMENT,
    FullCode TEXT NOT NULL UNIQUE,
    FunctionNo TEXT,
    TaskNo TEXT,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS org_OrganizationalUnit (
    OrgUnitId INTEGER PRIMARY KEY AUTOINCREMENT,
    Code TEXT,
    Name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_Dysponent (
    DysponentId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Notes TEXT
);

CREATE TABLE IF NOT EXISTS dbo_BudgetLine (
    BudgetLineId INTEGER PRIMARY KEY AUTOINCREMENT,
    BudgetPartId INTEGER,
    DzialId INTEGER,
    RozdzialId INTEGER,
    ParagrafId INTEGER,
    SourceId INTEGER,
    ExpenseGroupId INTEGER,
    BudgetTaskId INTEGER,
    OrgUnitId INTEGER,
    DysponentId INTEGER,
    Amount NUMERIC NOT NULL DEFAULT 0,

    FOREIGN KEY (BudgetPartId) REFERENCES ref_BudgetPart(BudgetPartId),
    FOREIGN KEY (DzialId) REFERENCES ref_Dzial(DzialId),
    FOREIGN KEY (RozdzialId) REFERENCES ref_Rozdzial(RozdzialId),
    FOREIGN KEY (ParagrafId) REFERENCES ref_Paragraf(ParagrafId),
    FOREIGN KEY (SourceId) REFERENCES ref_SourceOfFunding(SourceId),
    FOREIGN KEY (ExpenseGroupId) REFERENCES ref_ExpenseGroup(ExpenseGroupId),
    FOREIGN KEY (BudgetTaskId) REFERENCES ref_BudgetTask(BudgetTaskId),
    FOREIGN KEY (OrgUnitId) REFERENCES org_OrganizationalUnit(OrgUnitId),
    FOREIGN KEY (DysponentId) REFERENCES dim_Dysponent(DysponentId)
);
"""
)

cur.execute(
    "INSERT INTO ref_BudgetPart (PartCode, Name, IsGroup) VALUES (?, ?, ?)",
    ("01", "Kancelaria Prezydenta RP", 0),
)

cur.execute(
    "INSERT INTO ref_Dzial (DzialCode, Name) VALUES (?, ?)",
    ("101", "Administracja publiczna"),
)

cur.execute(
    "INSERT INTO ref_Rozdzial (RozdzialCode, DzialId, Name) VALUES (?, ?, ?)",
    ("1010", 1, "Wydatki administracyjne ogólne"),
)

cur.execute(
    "INSERT INTO ref_Paragraf (ParagrafCode, Name) VALUES (?, ?)",
    ("100", "Wynagrodzenia osobowe"),
)

cur.execute(
    "INSERT INTO ref_SourceOfFunding (SourceCode, Name) VALUES (?, ?)",
    ("1", "Środki własne"),
)

cur.execute(
    "INSERT INTO ref_ExpenseGroup (Name) VALUES (?)",
    ("Wynagrodzenia",),
)

cur.execute(
    "INSERT INTO ref_BudgetTask (FullCode, FunctionNo, TaskNo) VALUES (?, ?, ?)",
    ("06.03.01.04", "06", "03"),
)

cur.execute(
    "INSERT INTO org_OrganizationalUnit (Code, Name) VALUES (?, ?)",
    ("DIT", "Departament Informatyki"),
)

cur.execute(
    "INSERT INTO dim_Dysponent (Name) VALUES (?)",
    ("Dyrektor Finansowy",),
)

cur.execute(
    """
    INSERT INTO dbo_BudgetLine (
        BudgetPartId, DzialId, RozdzialId, ParagrafId, SourceId,
        ExpenseGroupId, BudgetTaskId, OrgUnitId, DysponentId, Amount
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 10000.00),
)


conn.commit()
conn.close()

print("Baza utworzona w:", DB_PATH)
