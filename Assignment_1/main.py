from fastapi import FastAPI, HTTPException

app = FastAPI()
@app.get("/")
async def root():
    return{"message": "The server is workingg!"}



'''@app.get("/health")
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
