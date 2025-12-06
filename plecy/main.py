#tu bedzie odpalanie uvicorna z reactem
#aktualny build jest tylko placeholderem na pozniej
#jest tu rowniez ogarniete logowanie uzytkownika
from fastapi import FastAPI, HTTPException,Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sqlite3

app = FastAPI()
#handlowanie polaczenia z baza - idk jak jeszcze bedzie dzialalo
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "baza" / "baza.db"

def get_db():
    if not DB_PATH.exists():
        print(f"UWAGA: baza nie istnieje: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@app.post("/login")
def login(data: dict, conn: sqlite3.Connection = Depends(get_db)):
    login = data.get("login")
    password = data.get("password")

    if not login or not password:
        raise HTTPException(status_code=400, detail="Brak loginu lub hasła")

    cur = conn.cursor()
    cur.execute(
        "SELECT id, login FROM users WHERE login = ? AND password = ?;",
        (login, password),
    )
    row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=401, detail="Nieprawidłowy login lub hasło")

    return {"login": row["login"]}


