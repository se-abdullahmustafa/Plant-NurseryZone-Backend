from sqlalchemy.orm import Session
from app.models.User import User as UserModel
from app.models.DeliveryBoy import DeliveryBoy as DeliverBoyModel
from app.schemas.user import UserCreateForDeliveryBoy
from fastapi import HTTPException

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
