import jwt
from fastapi import HTTPException, status, Request
from jwt import InvalidTokenError

from src.user.dtos import UserSchema, LoginSchema
from src.utils.settings import settings
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
from datetime import datetime, timedelta

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(body:UserSchema, db:Session):
    print(body)
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(status_code=400, detail="User already exists..")
    """Check email address"""
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(status_code=400, detail="Email Address already exists..")
    hash_password = get_password_hash(body.password)
    new_user = UserModel(
        name=body.name,
        username = body.username,
        email = body.email,
        hashed_password = hash_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(body:LoginSchema, db:Session):
    print(body)
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="User does not exist.")
    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Incorrect password.")

    #exp_time = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    exp_time = datetime.now() + timedelta(seconds=30)
    print(exp_time.timestamp())
    token = jwt.encode({"_id":user.id, "exp": exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)

    return {"token": token}

def is_authenticated(request: Request, db: Session):
    try:
        print(request.headers)
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")
        token = token.split(" ")[-1]
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        print(data)
        user_id = data.get("_id")
        exp_time = int(data.get("exp"))

        current_time = datetime.now().timestamp()

        print(exp_time - current_time)

        if current_time > exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
