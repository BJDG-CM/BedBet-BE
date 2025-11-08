from fastapi import APIRouter, Depends
from app.models.money_model import MoneyRequestDto
from app.libs.jwt import verify_token
from app.services.money_service import requestMoney, getMoneyPendingRequests, cancelRequestMoney, giveMoney

router = APIRouter()

@router.get('/requests/pending')
def get_money_pending_requests():
    return getMoneyPendingRequests()

@router.post('/request')
def request_money(moneyRequestDto: MoneyRequestDto, userUid = Depends(verify_token)):
    return requestMoney(moneyRequestDto, userUid)

@router.delete('/request/cancel')
def cancel_request_money(userUid = Depends(verify_token)):
    return cancelRequestMoney(userUid)

@router.post('/give/{userUid}')
def give_money(userUid: str):
    return giveMoney(userUid)

