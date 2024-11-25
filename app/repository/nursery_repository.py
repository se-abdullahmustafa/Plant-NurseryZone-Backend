from sqlalchemy import select
from app.schemas.nursery import NurseryCreate,NurseryResponse
from app.models.Nurseries import Nurseries as NurseryModel
from app.models.User import User as UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException


# def register_nursery(db:Session,nursery:NurseryCreate):
#     db_nursery=NurseryModel(user_id=nursery.user_id)
#     db.add(db_nursery)
#     db.commit()
#     db.refresh(db_nursery)
#     return db_nursery
# def get_nursery(db:Session,user_id:int):
#     return db.query(NurseryModel).filter(NurseryModel.user_id==user_id).first()
def get_nursery_requests(db:Session,pending_request:bool=True,skip:int=0,limit:int=20):
    nurseries = db.query(NurseryModel,UserModel).join(UserModel,NurseryModel.user_id==UserModel.user_id).filter(NurseryModel.status== "Pending" if pending_request else NurseryModel.status=="Accepted").order_by(UserModel.user_id).offset(skip).limit(limit=limit).all()
    if nurseries is None or len(nurseries)==0:
        raise HTTPException(status_code=404,detail="No nurseries request found")
    result = []
    for nursery, user in nurseries:
        nursery_dict = {
            "nursery_id": nursery.nursery_id,
            "name": user.name,
            "email": user.email,
            "address":user.address,
            "contact_number":user.contact_number,
            "status": nursery.status,
            "user_id": user.user_id,
            
        }
        result.append(nursery_dict)
    return result
def toggle_nursery_request(db:Session, nursery_id:int,is_accepted:bool):
    db_nursery=db.query(NurseryModel).filter(NurseryModel.nursery_id==nursery_id).first()
    if db_nursery is None:
        raise HTTPException(status_code=404,detail="Nursery not found")
    if is_accepted:
        db_nursery.status="Accepted"
    else:
        db_nursery.status="Rejected"
    db.commit()
    return {"message":"Status has been changed successfully."}    