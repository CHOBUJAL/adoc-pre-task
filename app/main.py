from datetime import datetime
from zoneinfo import ZoneInfo

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect

from app.routers.board_router import board_required_router, board_router
from app.routers.user_router import user_required_router, user_router

app = FastAPI()

connect(db='adoc', host='mongodb://adoc:adoc@mongodb-container.docker:27017/adoc?authSource=admin', maxPoolSize=100)

app.include_router(user_router)
app.include_router(user_required_router)
app.include_router(board_router)
app.include_router(board_required_router)

origins = [
    "http://localhost:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return datetime.now().astimezone(ZoneInfo("UTC"))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
