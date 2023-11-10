import httpx
import logging, logging.config

from fastapi import FastAPI, Request
from app import test

logging.config.fileConfig('./config/logging.conf')
logger = logging.getLogger('root')

# FAST API Router
app = FastAPI(
        title="Kiosk BackEnd",
        version="1.0.0",
        docs_url="/docs",# Swagger ui url 
        redoc_url="/redoc" # redoc ui url
        )
# redirect 방지
app.router.redirect_slashes = False

# add router like flask blueprint
app.include_router(test.router)

@app.middleware("http")
async def middle_test(request: Request, call_next):
    
        logger.info(f"[Before Request] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n"\
                f"({request.method}) URL : {request.url}\n[Headers] : {request.headers}\n[Bodys] : {request.body}")
        
        # before reqeust
        response = await call_next(request)
        # after request         
        
        logger.info(f"[After Reqeust] Code : {response.status_code} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        
        # real response
        return response

@app.get("/")
async def root():
	return "root test"

logger.info("############################## START ##############################")