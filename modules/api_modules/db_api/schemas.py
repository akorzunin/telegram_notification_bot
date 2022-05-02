from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Optional, Union
from modules.utils.util_classes import TresholdType
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from pydantic import BaseModel

# Rules
# Create
class RuleCreate(BaseModel):
    pair: str
    value: float
    TresholdType: TresholdType
    owner_id: int

    class Config:
        arbitrary_types_allowed = True

# Read
class RuleRead(BaseModel):
    id: int
    pair: str 
    value: float 
    TresholdType: TresholdType 
    owner_id: int 
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

# Update
class RuleUpdate(BaseModel):
    pair: Optional[Union[str, InstrumentedAttribute]]
    value: Optional[Union[float, InstrumentedAttribute]]
    TresholdType: Optional[Union[TresholdType, InstrumentedAttribute]]
    owner_id: Optional[Union[int, InstrumentedAttribute]]
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

# UpdateReq use as response model in FastAPI roures
class RuleUpdate(BaseModel):
    pair: Optional[str]
    value: Optional[float]
    TresholdType: Optional[TresholdType]
    owner_id: Optional[int]
    class Config:
        arbitrary_types_allowed = True

# Users
# Create
class UserCreate(BaseModel):
    username: str
    chat_id: int

# Read
class UserRead(BaseModel):
    id: int
    username: str
    chat_id: str
    rules: list[RuleRead]

    class Config:
        orm_mode = True

# cannon update users appearantly
# Update


# UpdateReq use as response model in FastAPI roures


### OLD SHEMAS
class AuctionItemBase(BaseModel):
    title: str
    # не обяхателоное для заполнения поле
    description: Optional[str] = None
    price: float
    is_start_price: bool
    photo: str
    owner_id: int
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now() + relativedelta(years=1)
    

class AuctionItemCreate(AuctionItemBase):
    '''Create item from API data and save it to database'''
    is_start_price: bool = True

class AuctionItemRead(AuctionItemBase):
    '''Read item from database'''
    id: int
    is_sold: bool
    end_date: datetime

    class Config:
        orm_mode = True

class AuctionItemUpdate(BaseModel):
    '''Update item in database from API data'''
    title: Optional[Union[str, InstrumentedAttribute]]
    description: Optional[Union[str, InstrumentedAttribute]]
    price: Optional[Union[float, InstrumentedAttribute, BinaryExpression]]
    is_start_price: Optional[Union[bool, InstrumentedAttribute]] = False
    owner_id: Optional[Union[float, InstrumentedAttribute]]
    is_sold: Optional[Union[bool, InstrumentedAttribute]] = False
    end_date: Optional[Union[datetime, InstrumentedAttribute]]

    class Config:
        require_by_default = False # use Required[] 
        arbitrary_types_allowed = True
        orm_mode = True

class AuctionItemUpdateReq(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    is_start_price: Optional[bool] = False
    owner_id: Optional[float]
    is_sold: Optional[bool] = False
    end_date: Optional[datetime]

class AuctionUserCreate(BaseModel):
    '''Create user from API data and save it to database'''
    username: str

class AuctionUserRead(BaseModel):
    '''Read user from database'''
    id: int
    username: str
    items: list[AuctionItemRead] = []

    class Config:
        orm_mode = True
