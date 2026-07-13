from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.tasks.dtos import TaskSchema, TaskResponseSchema
from src.utils.helpers import is_authenticated
from src.utils.db import get_db
from src.user.models import UserModel
from typing import List
from  sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
#from ..utils.redis_config import universal_key_builder, cache_wrapper


task_routes = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_routes.post("/create", response_model= TaskResponseSchema, status_code= status.HTTP_201_CREATED)
def create_task(body:TaskSchema, db:Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.create_task(body, db, user.id)


@task_routes.get("/all_tasks",response_model=List[TaskResponseSchema], status_code= status.HTTP_200_OK)
@cache(expire=300) # cache for 5 minutes
def get_all_tasks(db:Session =Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_tasks(db, user.id)


@task_routes.get("/get_task/{task_id}", response_model=TaskResponseSchema, status_code= status.HTTP_200_OK)
@cache(expire=300)
def get_task(task_id:int, db:Session =Depends(get_db)):
    return controller.get_one_task(task_id, db)

@task_routes.put("/update_task/{task_id}", status_code=status.HTTP_201_CREATED)
def update_task(task_id:int, body:TaskSchema, db: Session =Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.update_task(task_id, body, db, user.id)

@task_routes.delete("/delete_task/{task_id}", response_model=None, status_code= status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int, db: Session =Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.delete_task(task_id, db, user.id)