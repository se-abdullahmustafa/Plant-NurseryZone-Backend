from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserResponse,UserCreate
from app.repository.user_repository import create_user,get_user,get_all_user,login_user
from app.DBHandler import get_db

router = APIRouter()

@router.post("/user",response_model=UserResponse)
def register(user:UserCreate,db:Session=Depends(get_db)):
    return create_user(db=db,user=user)
@router.get("/user",response_model=UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    return get_user(db=db,user_id=user_id)
@router.get("/users",response_model=List[UserResponse])
def get_users(skip:int=0,limit:int=20,db:Session=Depends(get_db)):
    return get_all_user(db=db,skip=skip,limit=limit)
@router.get("/login",response_model=UserResponse)
async def login(email:str,password:str,db:Session=Depends(get_db)):
    return await login_user(db=db,email=email,password=password)