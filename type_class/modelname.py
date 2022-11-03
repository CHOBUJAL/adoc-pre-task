from enum import Enum
from typing import Optional
from pydantic import BaseModel

class ModelName(str, Enum):
	alexnet = "alexnet"
	resnet = "resnet"
	lenet = "lenet"

class Item(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    