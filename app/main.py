from datetime import datetime
from zoneinfo import ZoneInfo

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user_router import user_router, user_required_router

app = FastAPI()

app.include_router(user_router)
app.include_router(user_required_router)

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