from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

'''@app.get("/")
async def root():
    return{"message": "The server is workingg!"}



@app.get("/health")
async def root():
    return{"name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
        }'''


tasks = [
    {"id": 1, "title": "studying my IBM course", "done": True},
    {"id":2, "title": "finishing my flyrank assignment", "done": True},
    {"id":3, "title": "watering my flowers", "done": True}
]



@app.get("/tasks")
async def get_all_tasks():
    return tasks


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if task:
        return task
    
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

tasks = [
    {"id": 1, "title": "studying my IBM course", "done": True},
    {"id":2, "title": "finishing my flyrank assignment", "done": True},
    {"id":3, "title": "watering my flowers", "done": True}
]

class TaskCreate(BaseModel):
    title: str

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def POST_tasks(task_data: TaskCreate):
    cleaned_title = task_data.title.strip()
    if not cleaned_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty or missing."
        )

    
    next_id = max((t["id"] for t in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": cleaned_title,
        "done": False
    }

    tasks.append(new_task)
    return new_task



