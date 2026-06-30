from fastapi import Request, Depends, HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session
from src.utils.settings import settings
from src.utils.db import get_db
from jwt.exceptions import InvalidTokenError
from src.user.models import UserModel
import jwt

def is_authenticated(request: Request, db: Session = Depends(get_db)):
    try:
        #print(request.headers)
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")
        token = token.split(" ")[-1]
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

        user_id = data.get("_id")
        exp_time = int(data.get("exp"))

        current_time = datetime.now().timestamp()

        print(exp_time - current_time)
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")