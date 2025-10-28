import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .operations import add, subtract, multiply, divide

# --- Logging setup ---
LOG_DIR = Path("logs"); LOG_DIR.mkdir(exist_ok=True)
logger = logging.getLogger("calculator")
logger.setLevel(logging.INFO)

# File handler (rotating)
fh = RotatingFileHandler(LOG_DIR / "app.log", maxBytes=500_000, backupCount=3)
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s"))

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s"))

if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(ch)

app = FastAPI(title="FastAPI Calculator", version="1.0.0")

# Static + templates (for a minimal front-end)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("➡️ %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
        logger.info("⬅️ %s %s -> %s", request.method, request.url.path, response.status_code)
        return response
    except Exception as e:
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        raise e

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/add")
def api_add(a: float = Query(...), b: float = Query(...)):
    logger.info("add called with a=%s b=%s", a, b)
    return {"operation": "add", "a": a, "b": b, "result": add(a, b)}

@app.get("/api/subtract")
def api_subtract(a: float = Query(...), b: float = Query(...)):
    logger.info("subtract called with a=%s b=%s", a, b)
    return {"operation": "subtract", "a": a, "b": b, "result": subtract(a, b)}

@app.get("/api/multiply")
def api_multiply(a: float = Query(...), b: float = Query(...)):
    logger.info("multiply called with a=%s b=%s", a, b)
    return {"operation": "multiply", "a": a, "b": b, "result": multiply(a, b)}

@app.get("/api/divide")
def api_divide(a: float = Query(...), b: float = Query(...)):
    logger.info("divide called with a=%s b=%s", a, b)
    try:
        res = divide(a, b)
        return {"operation": "divide", "a": a, "b": b, "result": res}
    except ZeroDivisionError as e:
        logger.warning("division by zero: a=%s b=%s", a, b)
        raise HTTPException(status_code=400, detail=str(e))
