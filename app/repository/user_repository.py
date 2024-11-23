from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.User import User as UserModel
from app.schemas.user import UserCreate
from app.models.Nurseries import Nurseries as NurseryModel

def create_user(db:Session,user:UserCreate):
    db_user=UserModel(email=user.email,password_hash=user.password_hash,name=user.name,address=user.address,contact_number=user.contact_number)
    db.add(db_user)
    db.commit()
    if user.is_nursery:
        db_nursery=NurseryModel(user_id=db_user.user_id)
        db_user.role="Nursery"
        db.add(db_nursery)
        db.commit()
    db.refresh(db_user)
    return db_user
def login_user(db:Session,email:str,password:str):
    db_user=db.query(UserModel).filter(UserModel.email==email).filter(UserModel.password_hash==password).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail="invalid credential")
    return db_user
        
def get_user(db:Session,user_id:int):
    db_user = db.query(UserModel).filter(UserModel.user_id==user_id).first()
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=401, detail="User not found")

def get_all_user(db:Session,skip:int=0,limit:int=20):
    return db.query(UserModel).order_by(UserModel.user_id).offset(skip).limit(limit=limit).all()