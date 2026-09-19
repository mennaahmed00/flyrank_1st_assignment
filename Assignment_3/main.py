
from fastapi import FastAPI, HTTPException
from repository import init_db, get_all_tasks, get_task_by_id
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    init_db()
    yield
    # Runs on shutdown (if needed)


app = FastAPI(lifespan=lifespan)

@app.get("/tasks")
def read_tasks():
    return get_all_tasks()

@app.get("/tasks/{task_id}")
def read_single_task(task_id:int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code = 404, detail = {"error": "Task not found"})
    return task