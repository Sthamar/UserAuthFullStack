from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas.user import UserCreate, UserOut
from typing import List

router = APIRouter(prefix="/user", tags=["user"])

@router.post('/', response_model=UserOut)
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    existing_uesrname = db.query(User).filter(User.username == user.username).first()
    if existing_uesrname:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist")
    new_user = User(
        username = user.username,
        password = user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
