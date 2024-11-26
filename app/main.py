from fastapi import FastAPI
from pathlib import Path
import uvicorn
from app.routers import user_route,nursery_route,order_route

app = FastAPI(title="Nursery Plant Zone",description="Online Plateform to sell plants.")


app.include_router(router=user_route.router, prefix="/api", tags=["User"])
app.include_router(router=nursery_route.router, prefix="/api", tags=["Nursery"])
app.include_router(router=order_route.router,prefix="/api",tags=["Order"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)