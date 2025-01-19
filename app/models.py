from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class Invoice(BaseModel):
    reference: str | None
    beneficiary_name: str | None
    account_id: str | None
    amount: Decimal | None
    currency: str | None
    due_date: date | None