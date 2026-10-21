from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "server is running"}


import sqlite3


def inot_db():
    conn = sqlite3.connect("task_db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    is_done INTEGER DEFAULT 0)""")
    conn.commit()
    conn.close()


inot_db()


from pydantic import BaseModel


class TaskInput(BaseModel):
    title: str


@app.post("/tasks/")
def create_task(task: TaskInput):
    conn = sqlite3.connect("task_db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES  (?)", (task.title,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"id": new_id, "title": task.title}


@app.get("/tasks/")
def get_tasks():
    conn = sqlite3.connect("task_db")
    cursor = conn.cursor()
    cursor.execute("SELECT id , title  , is_done FROM tasks")
    row = cursor.fetchall()
    conn.close()

    return [{"id": r[0], "title": r[1], "is_done": r[2]} for r in row]


from fastapi import HTTPException


@app.get("/tasks/{task_id}")
def get_by_id(task_id: int):
    conn = sqlite3.connect("task_db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, is_done FROM  tasks WHERE id = (?)", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="task not found")
    return {"id": row[0], "title": row[1], "is_done": row[2]}


@app.delete("/tasks/{task_id}")
def delete_by_id(task_id:int):
    conn = sqlite3.connect("task_db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = (?)", (task_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="task not found")
    return {"message": "task deleted"}
