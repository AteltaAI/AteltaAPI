from fastapi import APIRouter
from routes.evaluate import router as evaluate_router

main_router = APIRouter()
main_router.include_router(evaluate_router, prefix="/v1/evaluate", tags=["evaluate"])


@main_router.get("/")
async def index():
    return {"Response status": 200, "Message": "Hello from AteltaAPI"}
