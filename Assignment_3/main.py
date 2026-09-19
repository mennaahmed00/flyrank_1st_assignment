
from fastapi import FastAPI, HTTPException,Response,status
from repository import init_db, get_all_tasks, get_task_by_id
from contextlib import asynccontextmanager
from pydantic import BaseModel

from repository import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    init_db,
    update_task,
)
class TaskCreate(BaseModel):
    title: str
    done: bool = False

class TaskUpdate(BaseModel):
    title: str
    done: bool

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

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def add_task(payload: TaskCreate):
    if not payload.title or not payload.title.strip():
        raise HTTPException(
            status_code = 400, detail = {"error": "Title cannot be empty"}
        )
    return create_task(title=payload.title.strip(), done=payload.done)


@app.put("/tasks/{task_id}")
def edit_task(task_id: int, payload: TaskUpdate):
    if not payload.title or not payload.title.strip():
        raise HTTPException(
            status_code=400, detail={"error":"Title cannot be empty"}
                            )
    updated = update_task(task_id, payload.title.strip(), payload.done)
    if updated is None:
        raise HTTPException(
            status_code=404,detail={"error":"Task not found"}
        )
    return updated
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int):
    success = delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=404, detail={"error":"Task not found"}
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)