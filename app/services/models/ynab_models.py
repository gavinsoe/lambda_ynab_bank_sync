from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Budget(BaseModel):
    id: str
    name: str
    last_modified_on: datetime

class Account(BaseModel):
    id: str
    name: str
    type: str
    on_budget: bool
    closed: bool
    balance: float
    cleared_balance: float
    
class Transaction(BaseModel):
    id: Optional[str]
    date: str
    amount: int
    payee_id: Optional[str]
    payee_name: Optional[str]
    category_id: Optional[str]
    memo: Optional[str]
    cleared: str
    
    def __eq__(self, other: object) -> bool:        
        if not isinstance(other, Transaction):
            # don't attempt to compare against unrelated types
            return NotImplemented

        # if both have id, then compare that
        if self.id and other.id and self.id == other.id:
            return True
        
        # otherwise compare fields
        return self.date == other.date and self.amount == other.amount
