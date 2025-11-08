from pydantic import BaseModel

class CoinRequestDto(BaseModel):
    amount: int
