from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel

class FileDownloadBody(BaseModel):
    company_id: str
    store_id: str
    device_id: str
    mdfive: str
    force: int = 0

class FileUploadBody(BaseModel):
    company_id: str = None
    store_id: str = None
    device_id: str = None
    
class LogBody(BaseModel):
    company_id: str
    store_id: str
    device_id: str
    mdfive: str
    date: str
    time: str
    force: int = 0
    
class OptionBody(BaseModel):
    store_option: int
    device_option: int