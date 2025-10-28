# FastAPI Calculator

A small FastAPI app with unit, integration, and Playwright end-to-end tests, plus logging and CI.

## Run locally

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps
uvicorn app.main:app --reload
