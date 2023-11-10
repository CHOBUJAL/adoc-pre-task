from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel

class ModelTest(BaseModel):
    a: str
    b: Union[str, None] = None
    c: Optional[str] = None