from pydantic import BaseModel

class MoneyRequestDto(BaseModel):
    amount: int
