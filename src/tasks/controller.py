from fastapi import HTTPException

from src.tasks.dtos import TaskSchema, TaskResponseSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel


def get_task_or_404(db:Session, task_id:int):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(404, detail="Task not found, Task Id is Incorrect")
    return task

def create_task(body:TaskSchema, db:Session, user_id:int):
    print(body.model_dump())
    data = body.model_dump()
    #return controller.create_task(body)
    new_task = TaskModel(title = data["title"], description = data["description"], is_completed = data["is_completed"], user_id = user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db:Session, user_id:int):
    tasks = db.query(TaskModel).all()
    return tasks

def get_one_task(task_id:int, db:Session) -> HTTPException | type[TaskModel]:
    return get_task_or_404(db, task_id)

def update_task(task_id:int, body:TaskSchema, db:Session, user_id:int)-> type[TaskModel]:
    one_task = get_task_or_404(db, task_id)
    # one_task.title = body.title
    # one_task.description = body.description
    # one_task.is_completed = body.is_completed
    print("debug 2")
    if one_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="You are not allowed to Update this task")
    print("debug 3")
    body = body.model_dump()
    for field, value in body.items():
        setattr(one_task, field, value)
    db.add(one_task)
    db.commit()
    db.refresh(one_task)
    return one_task

def delete_task(task_id:int, db:Session, user_id:int):
    one_task = get_task_or_404(db, task_id)
    if one_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="You are not allowed to Delete this task")
    db.delete(one_task)
    db.commit()
    return None