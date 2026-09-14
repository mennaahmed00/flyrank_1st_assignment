from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()




#first end point
@app.get("/")
async def root():
    return{"message": "The server is workingg!"}






# GET /health end point
@app.get("/health")
async def root():
    return{"name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
        }





#in-memory dictionnary
tasks = [
    {"id": 1, "title": "studying my IBM course", "done": True},
    {"id":2, "title": "finishing my flyrank assignment", "done": True},
    {"id":3, "title": "watering my flowers", "done": True}
]




#GET /tasks end point
@app.get("/tasks")
async def get_all_tasks():
    return tasks

#2nd GET endpoint /tasks/{tasks_id}
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if task:
        return task
    
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")



class TaskCreate(BaseModel):
    title: str




#POST /tasks end point
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



class taskUpdate(BaseModel):
    title: Optional[str]= None
    done: Optional[bool] = None

#Add PUT /tasks/:id
#checks the request body and filling it's valus in the title and done


#PUT /tasks/{task_id} end point
@app.put("/tasks/{task_id}")
async def put_task(task_id : int, body:taskUpdate):

    #checking if the body is empty
    if body.title is None and body.done is None:
        raise HTTPException(status_code = 400, detail = "Empty or invalid request body")

    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        raise HTTPException(status_code = 404, detail = "task not found")
    if body.title is not None:
        task["title"]= body.title
    if body.done is not None:
        task["done"] = body.done

    return task




#DELETE /tasks/{task_id} end point
@app.delete("/tasks/{task_id}",status_code = status.HTTP_204_NO_CONTENT)
async def deleteTask(task_id : int):
       for index,task in enumerate(tasks):
            if task["id"] == task_id:
                tasks.pop(index)
                return
            raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail= "Task not found")

