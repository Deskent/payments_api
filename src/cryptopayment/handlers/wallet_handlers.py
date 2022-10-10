from fastapi import APIRouter, Request

from models import Wallet
from schemas.data_schemas import DataStructurePaymentResult, DataStructureWallet
from services import get_or_create_wallet, check_payment_and_send_money
from schemas import CheckPayment, WalletIn_Pydantic
from services.utils import check_token

wallet_router = APIRouter()


@wallet_router.get("/get_wallet/{telegram_id}", tags=['wallet'], response_model=DataStructureWallet)
async def get_wallet(telegram_id: int, request: Request) -> DataStructureWallet:
    await check_token(request)

    wallet_obj: Wallet = await get_or_create_wallet(telegram_id)
    result = DataStructureWallet()
    result.status = 200
    result.success = True
    result.data = await WalletIn_Pydantic.from_tortoise_orm(wallet_obj)
    return result


@wallet_router.post("/check_payment", tags=['wallet'], response_model=DataStructurePaymentResult)
async def check_payment(data: CheckPayment, request: Request) -> DataStructurePaymentResult:
    await check_token(request)

    return await check_payment_and_send_money(data)
