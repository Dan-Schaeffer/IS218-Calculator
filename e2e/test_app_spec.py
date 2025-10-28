import pytest
from threading import Thread
import uvicorn
import time
import os

# Run the ASGI server in-process for E2E (port 8000)
def run_server():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, log_level="warning")

@pytest.fixture(scope="session", autouse=True)
def server():
    t = Thread(target=run_server, daemon=True)
    t.start()
    # give server a moment
    time.sleep(1.0)
    yield
    # daemon thread ends with test session

@pytest.mark.parametrize(
    "a,b,op,expect",
    [
        ("2", "3", "add", "Result: 5.0"),
        ("9", "2", "divide", "Result: 4.5"),
        ("3", "2.5", "multiply", "Result: 7.5"),
    ],
)
def test_happy_paths(page, a, b, op, expect):
    page.goto("http://127.0.0.1:8000/")
    page.fill("#a", a)
    page.fill("#b", b)
    page.select_option("#op", op)
    page.click("#go")
    page.wait_for_selector("#result")
    assert page.locator("#result").inner_text() == expect

def test_divide_by_zero(page):
    page.goto("http://127.0.0.1:8000/")
    page.fill("#a", "3")
    page.fill("#b", "0")
    page.select_option("#op", "divide")
    page.click("#go")
    page.wait_for_selector("#result")
    txt = page.locator("#result").inner_text()
    assert "Error 400: Division by zero" in txt
