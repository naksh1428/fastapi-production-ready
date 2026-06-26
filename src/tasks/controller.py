from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel


def create_task(body:TaskSchema, db:Session):
    print(body.model_dump())
    data = body.model_dump()
    #return controller.create_task(body)
    new_task = TaskModel(title = data["title"], description = data["description"], is_completed = data["is_completed"])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return{"Status":"Task Created", "data":new_task}