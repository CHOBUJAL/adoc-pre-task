from fastapi import APIRouter
import datetime

from app.type_clss import *


router = APIRouter(
    prefix="/chs",
    responses={404: {"description": "Not found"}}
    )

@router.get("/{test}")
async def get_test(test: str):
    return f"Input {test}"

@router.post("/one")
async def one(item: Item):
    return {"model_name": item.companyId, "message": item.storeId}

@router.get("/")
async def root():
	return "chs router check"
