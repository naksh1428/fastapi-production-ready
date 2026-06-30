from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.user import controller
from src.user.dtos import UserSchema
from src.utils.db import get_db
user_routes = APIRouter(prefix="/user")

@user_routes.post("/register", status_code= status.HTTP_201_CREATED)
def register(body:UserSchema, db:Session=Depends(get_db)):
    return controller.register(body, db)