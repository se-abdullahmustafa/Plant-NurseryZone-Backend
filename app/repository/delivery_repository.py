from sqlalchemy.orm import Session
from app.models.User import User as UserModel
from app.models.DeliveryBoy import DeliveryBoy as DeliverBoyModel
from app.models.DeliverySchedule import DeliverySchedule as DsModel
from app.schemas.user import UserCreateForDeliveryBoy
from fastapi import HTTPException
from datetime import datetime
from app.repository.nursery_repository import *

async def post_delivery_boy(db:Session,user:UserCreateForDeliveryBoy):
    if user is None:
        raise HTTPException(status_code=400,detail="Bad Request")
    db_user=UserModel(email=user.email,password_hash=user.password_hash,name=user.name,address=user.address,contact_number=user.contact_number,role="DeliveryBoy")
    try:
        db.add(db_user)
        db.commit()
        db_deliver_boy=DeliverBoyModel(nursery_id=user.nursery_id,user_id=db_user.user_id)
        db.add(db_deliver_boy)
        db.commit()
        return {"message":"Delivery Boy Added Successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))

async def get_deliver_boys(db:Session,nursery_id:int):
    nursery=await get_nursery_by_user_id(db,nursery_id)
    delivery_boys=db.query(DeliverBoyModel,UserModel).join(UserModel,DeliverBoyModel.user_id==UserModel.user_id).filter(DeliverBoyModel.nursery_id==nursery.nursery_id).all()
    if not delivery_boys:
        raise HTTPException(status_code=404,detail="Delivery Boy not found")
    result=[]
    for boy,user in delivery_boys:
        result.append({
            "user_id":user.user_id,
            "delivery_boy_id":boy.delivery_boy_id,
            "name":user.name
        })
    return result    
async def scheduled_delivery(db:Session,delivery_boy_id:int,order_id:int):
    schedule_date=datetime.now().today().strftime("%Y-%m-%d")
    dsModel=DsModel(order_id=order_id,scheduled_date=schedule_date,delivery_boy_id=delivery_boy_id)
    try:
        db.add(dsModel)
        db.commit()
        db.refresh(dsModel)
        return {"message":"Delivery Scheduled Successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
