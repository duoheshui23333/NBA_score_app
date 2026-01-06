from fastapi import FastAPI
from app.service import start_background

app = FastAPI()

@app.on_event("startup")
def boot():
    start_background()

@app.get("/health")
def health():
    return {"status": "ok"}
