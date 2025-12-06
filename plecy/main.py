#tu bedzie odpalanie uvicorna z reactem
#aktualny build jest tylko placeholderem na pozniej
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

#paths
FRONTEND_DIR = Path(__file__).parent.parent / "ui" / "dist"

app = FastAPI()



@app.get("/", response_class=FileResponse)
async def home():
    return FileResponse(FRONTEND_DIR / "index.html")


