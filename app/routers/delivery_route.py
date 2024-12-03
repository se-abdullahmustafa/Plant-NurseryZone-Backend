from fastapi import APIRouter,HTTPException,Depends
from fastapi.responses import JSONResponse
from app.DBHandler import get_db
from app.schemas.user import UserCreateForDeliveryBoy
from app.repository.delivery_repository import *

router=APIRouter()

@router.post("/delivery/boy",response_class=JSONResponse)
async def add_delivery_boy(user:UserCreateForDeliveryBoy,db:Session=Depends(get_db)):
    return await post_delivery_boy(db=db,user=user)
@router.get("/delivery/boy",response_class=JSONResponse)
async def get_delivery_boys(nursery_id:int,db:Session=Depends(get_db)):
    return await get_deliver_boys(db,nursery_id)  
@router.post("/delivery/schedule",response_class=JSONResponse)
async def schedule_delivery(delivery_boy_id:int,order_id:int,db:Session=Depends(get_db)):
    return await scheduled_delivery(db,delivery_boy_id,order_id)  