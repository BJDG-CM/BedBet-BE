from fastapi import APIRouter, Depends
from app.models.coin_model import CoinRequestDto
from app.libs.jwt import verify_token
from app.services.coin_service import requestCoin, giveCoin, cancelRequestCoin, getCoinPendingRequests

router = APIRouter()

@router.get('/requests/pending')
def get_coin_pending_requests():
    return getCoinPendingRequests()

@router.post('/request')
def request_coin(coinRequestDto: CoinRequestDto, userUid = Depends(verify_token)):
    return requestCoin(coinRequestDto, userUid)

@router.delete('/request/cancel')
def cancel_request_coin(userUid = Depends(verify_token)):
    return cancelRequestCoin(userUid)

@router.post('/give/{userUid}')
def give_coin(userUid: str):
    return giveCoin(userUid)

