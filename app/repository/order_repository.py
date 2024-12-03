from fastapi import HTTPException
from app.models.Order import Order as OrderModel
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate
from app.models.Order import OrderStatusService
from app.models.Plant import Plant as PlantModel
from app.models.User import User as UserModel
from app.repository.nursery_repository import get_plant_by_id,decrease_stock,get_nursery_by_user_id
from datetime import datetime

async def add_order(db:Session,order:OrderCreate):
    plant= await get_plant_by_id(db,order.plant_id)
    if plant.stock<order.quantity:
        raise HTTPException(status_code=500,detail="Insufficient Quantity")
    new_order=OrderModel(user_id=order.user_id,plant_id=order.plant_id,quantity=order.quantity,total_amount=order.quantity*int(plant.price),created_at=datetime.now())
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        await decrease_stock(db,order.quantity,order.plant_id)
        return {"Order Placed Successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))    
    
async def get_all_order(db:Session,nursery_id:int,skip:int=0,limit:int=20):
    nursery= await get_nursery_by_user_id(db,user_id=nursery_id)
    orders=db.query(OrderModel,PlantModel).join(PlantModel,OrderModel.plant_id==PlantModel.plant_id).filter(PlantModel.nursery_id==nursery.nursery_id).filter(OrderModel.status=="Pending").order_by(OrderModel.created_at).offset(skip).limit(limit).all()
    result=[]
    await get_order_by_id(db,order_id=1)
    for order,plant in orders:
        result.append({"order_id":order.order_id,"Plant name":plant.name,"qunatity":order.quantity,"Total Amount":order.total_amount,"Status":order.status,"Created_at":order.created_at})
    return result
async def get_all_order_by_user_id(db:Session,user_id:int,skip:int=0,limit:int=20):
    orders=db.query(OrderModel,PlantModel).join(PlantModel,OrderModel.plant_id==PlantModel.plant_id).filter(OrderModel.user_id==user_id).order_by(OrderModel.created_at).offset(skip).limit(limit).all()
    result=[]
    await get_order_by_id(db,order_id=1)
    for order,plant in orders:
        result.append({"order_id":order.order_id,"Plant name":plant.name,"qunatity":order.quantity,"Total Amount":order.total_amount,"Status":order.status,"Created_at":order.created_at})
    return result
async def get_order_by_id(db:Session,order_id:int):
    order_detail = db.query(OrderModel,PlantModel,UserModel).join(PlantModel,OrderModel.plant_id==PlantModel.plant_id)\
        .join(UserModel,OrderModel.user_id==UserModel.user_id).filter(OrderModel.order_id==order_id).first()
    if not order_detail:
        raise HTTPException(status_code=404,detail="Order Details not found.")
    user={"name":order_detail[2].name,"address":order_detail[2].address,"contact_number":order_detail[2].contact_number}    
    return {"order_id":order_detail[0].order_id,"Plant name":order_detail[1].name,"qunatity":order_detail[0].quantity,"Total Amount":order_detail[0].total_amount,"Status":order_detail[0].status,"Created_at":order_detail[0].created_at,"customer":user}

async def change_order_status(order_id:int,status:str,db:Session):
        order=db.query(OrderModel).filter(OrderModel.order_id==order_id).first()
        if not order:
            raise HTTPException(status_code=404,detail="Order not found")
        if not OrderStatusService.validate_status_change(order.status, status):
            raise HTTPException(status_code=400,detail=f"Invalid status transition from {order.status} to {status}")
        order.status=status
        try:
            db.commit()
            db.refresh(order)
            return {"message":"Order status change successfully."}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500,detail=str(e))