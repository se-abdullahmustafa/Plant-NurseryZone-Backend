from fastapi import HTTPException
from app.models.Order import Order as OrderModel
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate
from app.models.Plant import Plant as PlantModel
from app.models.User import User as UserModel
from app.repository.nursery_repository import get_plant_by_id,decrease_stock
from datetime import datetime

async def add_order(db:Session,order:OrderCreate):
    plant= await get_plant_by_id(db,order.plant_id)
    if plant.stock<order.quntity:
        raise HTTPException(status_code=500,detail="Insufficient Quantity")
    new_order=OrderModel(user_id=order.user_id,plant_id=order.plant_id,quantity=order.quntity,total_amount=order.quntity*int(plant.price),created_at=datetime.now())
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        await decrease_stock(db,order.quntity,order.plant_id)
        return {"Order Placed Successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))    
    
async def get_all_order(db:Session,nursery_id:int,skip:int=0,limit:int=20):
    orders=db.query(OrderModel,PlantModel).join(PlantModel,OrderModel.plant_id==PlantModel.plant_id).filter(PlantModel.nursery_id==nursery_id).filter(OrderModel.status=="Pending").order_by(OrderModel.created_at).offset(skip).limit(limit).all()
    result=[]
    for order,plant in orders:
        result.append({"order_id":order.order_id,"Plant name":plant.name,"qunatity":order.quantity,"Total Amount":order.total_amount,"Status":order.status,"Created_at":order.created_at})
    return result
async def get_order_by_id(db:Session,order_id:int):
    order=db.query(OrderModel,PlantModel,)