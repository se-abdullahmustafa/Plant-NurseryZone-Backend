from fastapi import APIRouter,HTTPException,Depends
from fastapi.responses import JSONResponse
from app.DBHandler import get_db
from app.schemas.user import UserCreateForDeliveryBoy
from app.repository.delivery_repository import *

router=APIRouter()

@router.post("/delivery/boy",response_class=JSONResponse)
async def add_delivery_boy(user:UserCreateForDeliveryBoy,db:Session=Depends(get_db)):
    return await post_delivery_boy(db=db,user=user)
    