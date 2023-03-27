from fastapi import FastAPI

from app import models

# FAST API
app = FastAPI(responses={404: {"description": "Not found"}})
app.include_router(models.router)

@app.get("/")
async def root():
	return {"return": "root"}