from app.schemas.nursery import NurseryCreate,NurseryResponse
from app.models.Nurseries import Nurseries as NurseryModel
from sqlalchemy.orm import Session

# def register_nursery(db:Session,nursery:NurseryCreate):
#     db_nursery=NurseryModel(user_id=nursery.user_id)
#     db.add(db_nursery)
#     db.commit()
#     db.refresh(db_nursery)
#     return db_nursery
# def get_nursery(db:Session,user_id:int):
#     return db.query(NurseryModel).filter(NurseryModel.user_id==user_id).first()