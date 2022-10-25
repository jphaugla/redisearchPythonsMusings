from typing import Optional
from pydantic import StrictInt, EmailStr
from redis_om import Field, HashModel
from StrictDate import StrictDate
import datetime


class Customer(HashModel):
    first_name: str
    last_name: str = Field(index=True)
    email: EmailStr
    # this caused problems returning data from index searches
    # join_date: StrictDate
    join_date: datetime.date
    #   caused problems returning data from index searches
    #    age: int = Field(index=True)
    age: int = Field(index=True)
    bio: Optional[str] = "Super dope"
