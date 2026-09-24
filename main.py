from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# fake DB 
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Complete backend assignment", "done": False},
    {"id": 3, "title": "Walk the dog", "done": True},
]


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})


@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return find_task(task_id)


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    title = task_data.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail={"error": "Title cannot be empty"})

    # just bump off the last id 
    new_id = tasks[-1]["id"] + 1 if tasks else 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    task = find_task(task_id)

    if task_update.title is not None:
        title = task_update.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail={"error": "Title cannot be empty"})
        task["title"] = title

    if task_update.done is not None:
        task["done"] = task_update.done

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    task = find_task(task_id)
    tasks.remove(task)
