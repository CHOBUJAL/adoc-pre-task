from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel


class Item(BaseModel):
	name: Optional[str] = None
	age: Optional[dict] = None
