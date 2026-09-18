import sqlite3
from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel

app = FastAPI()

@app.get("/tasks")
async def get_tasks():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()
    task_list = []
    for row in rows:
        task_dict = {
            "id": row[0],
            "title": row[1],
            "done":bool(row[2])
        }
        task_list.append(task_dict)
    connection.close()
    return task_list

@app.get("/tasks/{task_id}")
async def get_task(task_id :int):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    #row = (1, 'watering my flowers', 1)
    ()
        
    cursor.execute("SELECT * from tasks WHERE id = ?",(task_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code = 404, detail = "Task not found")
    
    return {
            "id": row[0],
            "title" : row[1],
            "done": bool(row[2])
        }




class TaskCreate(BaseModel):
    title: str



@app.post("/tasks")
async def create_tasks(task_data: TaskCreate):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?,?)", (task_data.title,0) )
    task_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return{
        "id": task_id,
        "title": task_data.title,
        "done": False
    }

@app.delete("/tasks/{task_id}")
async def delete_task(task_id : int):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?" ,(task_id,))
    if cursor.rowcount == 0:
         connection.close()
         raise HTTPException(status_code=404, detail="Task not found")
    connection.commit()
    connection.close()


class TaskUpdate(BaseModel):
    title:str
    done: bool

@app.put("/tasks/{task_id}")
async def put_task(task_id : int ,task_data: TaskUpdate):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (task_data.title, task_data.done, task_id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code = 404, detail = "task not found")

    connection.commit()
    connection.close()
    
    return{
        "id": task_id,
        "title": task_data.title,
        "done": task_data.done
    }

    












