from fastapi import HTTPException
from app.models.Feedback import Feedback as FeedbackModel
from app.models.Order import Order as OrderModel
from app.models.User import User as UserModel
from app.models.Plant import Plant as PlantModel
from app.schemas.feedback import FeedbackCreate
from sqlalchemy.orm import Session
from app.repository.order_repository import get_order_by_id
from app.repository.nursery_repository import get_plant_by_id,get_nursery_by_user_id
from datetime import datetime

async def add_feedback(db:Session,feedback:FeedbackCreate):
    await get_order_by_id(db,feedback.order_id)
    create_at=datetime.now().today().strftime("%Y-%m-%d")
    new_feedback=FeedbackModel(order_id=feedback.order_id,comment=feedback.comment,created_at=create_at)
    try:
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        return {"message":"Feedback submit successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))   
    
async def get_feedback_by_plant_id(db:Session,plant_id:int):
    await get_plant_by_id(db,plant_id)
    feedbacks=db.query(FeedbackModel,OrderModel,UserModel).join(OrderModel,FeedbackModel.order_id==OrderModel.order_id)\
        .join(UserModel,UserModel.user_id==OrderModel.user_id).filter(OrderModel.plant_id==plant_id).all()
    result=[]
    for feedback,order,user in feedbacks:
        result.append({"name":user.name,"comment":feedback.comment,"created_at":feedback.created_at})
    return result    
            
async def get_feedback_by_nursery_id(db:Session,nursery_id:int):
    nursery=await get_nursery_by_user_id(db,nursery_id)
    feedbacks=db.query(FeedbackModel,OrderModel,UserModel,PlantModel).join(OrderModel,FeedbackModel.order_id==OrderModel.order_id)\
        .join(UserModel,UserModel.user_id==OrderModel.user_id).join(PlantModel,OrderModel.plant_id==PlantModel.plant_id).filter(PlantModel.nursery_id==nursery.nursery_id).all()
    result=[]

    for feedback,order,user,plant in feedbacks:
        result.append({"name":user.name,"comment":feedback.comment,"created_at":feedback.created_at,"order_id":order.order_id,"plant name":plant.name})
    return result    