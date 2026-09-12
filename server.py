import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# 1. تحميل متغيرات البيئة من ملف .env

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DEBUG: Connecting to {DATABASE_URL}")  # ضيفي السطر ده للتأكد
app = FastAPI()

def get_db_connection():
    # استخدام dict_row لترجيع النتايج كـ Dictionary زي row_factory في SQLite
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # إنشاء الجدول بأسلوب Postgres (SERIAL بدلاً من AUTOINCREMENT)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                );
            """)
            
            # التأكد إن الجدول فاضي قبل إضافة البيانات الأولية
            cur.execute("SELECT COUNT(*) FROM tasks;")
            count = cur.fetchone()["count"]
            
            if count == 0:
                cur.executemany("""
                    INSERT INTO tasks (title, done) VALUES (%s, %s);
                """, [
                    ("Setup Postgres Database", False),
                    ("Read FastAPI Documentation", True),
                    ("Complete Backend Assignment", False)
                ])
            conn.commit()

# تشغيل التهيئة عند بدء التطبيق
init_db()

class TaskCreate(BaseModel):
    title: str
    done: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/tasks")
def get_tasks():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks;")
            tasks = cur.fetchall()
            return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
            task = cur.fetchone()
            if task is None:
                raise HTTPException(status_code=404, detail="Task not found")
            return task

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # جلب الـ ID الجديد مباشرة باستخدام RETURNING id
            cur.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id;",
                (task.title, task.done or False)
            )
            new_id = cur.fetchone()["id"]
            conn.commit()
            return {"id": new_id, "title": task.title, "done": task.done}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
            task = cur.fetchone()
            if task is None:
                raise HTTPException(status_code=404, detail="Task not found")
            
            new_title = task_update.title if task_update.title is not None else task["title"]
            new_done = task_update.done if task_update.done is not None else task["done"]
            
            cur.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s;",
                (new_title, new_done, task_id)
            )
            conn.commit()
            return {"id": task_id, "title": new_title, "done": new_done}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
            task = cur.fetchone()
            if task is None:
                raise HTTPException(status_code=404, detail="Task not found")
            
            cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
            conn.commit()
            return {"message": "Task deleted successfully", "task": task}