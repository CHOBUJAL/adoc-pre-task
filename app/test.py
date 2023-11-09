from typing import Union, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

import logging, logging.config
import time

logging.config.fileConfig('./config/logging.conf')
logger = logging.getLogger('test')

# Create Router like Flask Blue-print
router = APIRouter(prefix="/test")

async def background_test():
    for i in range(5):
        logger.info(i)
        time.sleep(0.1)
        
async def dependTest(a: str, b: str):
    return {'a': a, 'b': b}
    
    
@router.get(path="/depends", description="Dependencies Test API")
async def TestDependencies(dt: dict = Depends(dependTest)):
    return dt


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

logger.info("############################## START ##############################")