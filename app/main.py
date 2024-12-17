from datetime import datetime
from zoneinfo import ZoneInfo

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:18001",
    "http://192.168.1.106:18001",
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


@app.get('/favicon.ico')
async def favicon():
    return JSONResponse(status_code=204)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)