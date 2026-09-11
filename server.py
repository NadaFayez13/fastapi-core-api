import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

DB_NAME = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    if count == 0:
        cursor.executemany("""
            INSERT INTO tasks (title, done) VALUES (?, ?)
        """, [
            ("Setup SQLite Database", 0),
            ("Read FastAPI Documentation", 1),
            ("Complete Backend Assignment", 0)
        ])
    
    conn.commit()
    conn.close()

init_db()

class TaskCreate(BaseModel):
    title: str
    done: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [dict(task) for task in tasks]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return dict(task)

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, int(task.done or False))
    )
    conn.commit()
    new_id = cursor.lastrowid 
    conn.close()
    
    return {"id": new_id, "title": task.title, "done": task.done}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    conn = get_db_connection()
    
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
     
    new_title = task_update.title if task_update.title is not None else task["title"]
    new_done = task_update.done if task_update.done is not None else task["done"]
    
     
    conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (new_title, int(new_done), task_id)
    )
    conn.commit()
    conn.close()
    
    return {"id": task_id, "title": new_title, "done": bool(new_done)}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Task deleted successfully", "task": dict(task)}