from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.DBHandler import get_db
from app.schemas.order import *
from app.repository.order_repository import *
from typing import List

router=APIRouter()

@router.post("/order",response_class=JSONResponse)
async def place_order(order:OrderCreate,db:Session=Depends(get_db)):
    return await add_order(db,order)
@router.get("/order",response_class=JSONResponse)
async def get_orders(nursery_id:int,skip:int=0,limit:int=20,db:Session=Depends(get_db)):
    return await get_all_order(db,nursery_id,skip,limit)
@router.get("/order/{user_id}",response_class=JSONResponse)
async def get_orders(user_id:int,skip:int=0,limit:int=20,db:Session=Depends(get_db)):
    return await get_all_order_by_user_id(db,user_id,skip,limit)
@router.get("/order/{order_id}",response_class=JSONResponse)
async def get_order_details(order_id:int,db:Session=Depends(get_db)):
    return await get_order_by_id(db,order_id)
@router.put("/order/status",response_class=JSONResponse)
async def update_order_status(order_id:int,status:str,db:Session=Depends(get_db)):
    return await change_order_status(order_id,status,db)