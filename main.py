from fastapi import FastAPI

from app import models

# FAST API Router
app = FastAPI(
        responses={404: {"description": "Not found"}},
        )
# redirect 방지
app.router.redirect_slashes = False
app.include_router(models.router)

@app.get("/")
async def root():
	return "/"