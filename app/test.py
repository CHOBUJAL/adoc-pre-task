from typing import Union, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Path, Query
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from common import models
import logging, logging.config
import time
import copy

logging.config.fileConfig('./config/logging.conf')
logger = logging.getLogger('test')

# Create Router like Flask Blue-print
router = APIRouter(prefix="/test")

class FakeDB:
    def __init__(self):
        self.data = dict()
        
    def clear():
        self.data = dict()

async def background_test():
    for i in range(5):
        logger.info(i)
        time.sleep(0.1)
        
async def dependTest():
    db = FakeDB()
    try:
        yield db
    finally:
        db.clear()
        
@router.get(path="/apikey", description="X-API-Key Test API")
async def TestApiKey(api_key_header: str=Depends(APIKeyHeader(name="X-API-Key"))):
    if api_key_header != "123":
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
    return {'api key': api_key_header}
    
@router.get(path="/depends", description="Dependencies Test API")
async def TestDependencies(a: str, b: str, fakedb: FakeDB = Depends(dependTest)):
    fakedb.data['a'] = a
    fakedb.data['b'] = b
    fakedb.data['Dependencies Test API'] = "Dependencies Test API"
    return JSONResponse(content=fakedb.data, status_code=202)


@router.get(path="/query", description="Query Parameter Test API")
async def TestQueryParameter(a: str, b: str):
    return f"QueryParameter Test A: {a}, B: {b}"


@router.get(path="/background", description="Background Test API")
async def TestBackground(bt: BackgroundTasks):
    bt.add_task(background_test)
    return "Background Test"


@router.get(path="/path/{path_parameter}", description="Path Parameter Test API")
async def TestPathParameter(path_parameter):
    return f"PathParameter Test Path: {path_parameter}"

# return FileResponse(path=f"../kiosk_exe_zip/{real_file_name}", filename=real_file_name, status_code=result['status'], media_type="file/zip")
# async def uploadSignature(file: UploadFile)
logger.info("############################## START ##############################")