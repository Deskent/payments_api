import datetime

from fastapi import APIRouter, Response, Request
from starlette import status

from models.models import User, License, Statuses, Service
from schemas import UserTelegramID, User_Pydantic, UserCreate, WalletIn_Pydantic
from schemas.data_schemas import DataStructure
from services import get_or_create_wallet
from services.exceptions import UserExistsException, exception_not_found
from services.utils import check_token

user_router = APIRouter()


@user_router.post("/create_user", response_model=DataStructure, tags=['user'])
async def create_user(user: UserCreate, response: Response, request: Request):
    await check_token(request)

    result = DataStructure()
    if await User.exists(telegram_id=user.telegram_id):
        raise UserExistsException
    user_data = {
        'nick_name': user.nick_name,
        'telegram_id': user.telegram_id,
        'expired_at': datetime.datetime.now()
    }
    await User.create(**user_data)
    result.status = 200
    result.success = True
    result.data = {}
    response.status_code = status.HTTP_201_CREATED
    return result.as_dict()


@user_router.post("/activate_user", tags=['user'])
async def activate_user(data: UserTelegramID, request: Request) -> dict:
    await check_token(request)

    subscribe_time = datetime.timedelta(days=30)
    user: User = await User.get_or_none(telegram_id=data.telegram_id)
    time_left = user.expired_at.utcnow() - datetime.datetime.utcnow()
    time_left = time_left if time_left.days > 0 else datetime.timedelta()

    user.expired_at = datetime.datetime.utcnow() + subscribe_time + time_left
    user.status = Statuses.member

    await user.save()
    return {"result": user}


@user_router.post("/deactivate_user", tags=['user'])
async def deactivate_user(data: UserTelegramID, request: Request) -> dict:
    await check_token(request)

    result = await User.filter(telegram_id=data.telegram_id).update(status=Statuses.ex_member)
    return {"result": result}


@user_router.post("/set_user_admin", tags=['user'])
async def set_user_admin(data: UserTelegramID, request: Request)-> dict:
    await check_token(request)

    result = await User.filter(telegram_id=data.telegram_id).update(status=Statuses.admin)
    return {"result": result}


@user_router.post("/get_user_status", tags=['user'])
async def get_user_status(data: UserTelegramID, request: Request) -> dict:
    await check_token(request)

    user = await User.get_or_none(telegram_id=data.telegram_id)
    if user:
        return {"status": user.status}
    raise exception_not_found


@user_router.post("/get_user_licenses_info", tags=['user'])
async def get_user_licenses_info(data: UserTelegramID, request: Request) -> list[dict]:
    await check_token(request)

    query = License.filter(user__telegram_id=data.telegram_id).select_related("product")
    answer = await query.values(
        'created_at', 'expired_at', 'description', 'license', product='product__name',
        price='product__price', product_description='product__description'
    )

    return answer


@user_router.post("/get_user_list", response_model=list[User_Pydantic], tags=['user'])
async def get_user_list(request: Request) -> list:
    await check_token(request)

    return await User.all()


@user_router.get("/get_active_users", response_model=list[UserTelegramID], tags=['user'])
async def get_active_users(request: Request) -> list:
    await check_token(request)

    return await User.filter(status__in=[Statuses.member, Statuses.admin]).values('telegram_id')


@user_router.post("/buy_subscription", tags=['user'])
async def buy_subscribe(data: UserTelegramID, request: Request) -> dict:
    await check_token(request)
    service = await Service.first()
    if not service:
        raise exception_not_found
    user = await User.get_or_none(telegram_id=data.telegram_id)
    if not user:
        raise exception_not_found
    cost_usd = service.newbie_price
    if user.status in (Statuses.ex_member, Statuses.member):
        cost_usd = service.member_price
    elif user.status == Statuses.admin:
        cost_usd = 0
    result = DataStructure()
    wallet_obj = await get_or_create_wallet(data.telegram_id)
    result.success = True
    result.data = {
        "cost_usd": cost_usd,
        "wallet": await WalletIn_Pydantic.from_tortoise_orm(wallet_obj)
    }
    return result.as_dict()
