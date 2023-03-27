from fastapi import APIRouter

from app.type_clss import *


router = APIRouter(
    prefix="/models",
    responses={404: {"description": "Not found"}}
    )

@router.get("/")
async def root():
	return {"return": "models root"}

@router.get("/one")
async def one(item: Item):

    return {"model_name": model_name, "message": "Have some residuals"}