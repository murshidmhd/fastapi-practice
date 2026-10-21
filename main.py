from fastapi import FastAPI

import sqlite3

app = FastAPI()


from pydantic import BaseModel


@app.get("/")
def home():
    return {"message": "server is running"}


def init_db():
    conn = sqlite3.connect("user_form_db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL, email TEXT NOT NULL , message TEXT NOT NULL)"""
    )

    conn.commit()
    conn.close()


init_db()


class UserData(BaseModel):
    name: str
    email: str
    message: str


@app.post("/user")
def data_enter(data: UserData):
    conn = sqlite3.connect("user_form_db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user(name ,email, message) VALUES (?,?,?)",
        (data.name, data.email, data.message),
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"id": new_id, "data": data}


@app.get("/users")
def users():
    conn = sqlite3.connect("user_form_db")
    cursor = conn.cursor()
    print("in")
    cursor.execute("SELECT id ,name , email , message FROM  user")
    data = cursor.fetchall()
    print(f"data is in here" , data)
    conn.close()

    return [{"id": r[0], "name": r[1], "email": r[2], "message": r[3]} for r in data]
