from fastapi import FastAPI
from typing import Optional
app = FastAPI()   

@app.get("/")
def say_hello():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "ok😉"}

@app.get("/greet")
def greet(name: str="Nadosha"):
    return {"message": f"Hello, {name}🌹"}

@app.get("/add")
def add_numbers(a: int, b: int):
    return {
        "num1:": a,
        "num2:": b,
        "result": a + b}

@app.get("/search")
def search(q: str, category: Optional[str] = None, limit: Optional[int] = 10):
    return {
        "query": q,
        "category": category,
        "limit": limit
    }