from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel


class Item(BaseModel):
	companyId: Optional[str] = None
	storeId: Optional[str] = None
