from fastapi import FastAPI
import uvicorn
from app.routers import user_route,nursery_route

app = FastAPI(title="Nursery Plant Zone",description="Online Plateform to sell plants.")

app.include_router(router=user_route.router, prefix="/api", tags=["User"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)