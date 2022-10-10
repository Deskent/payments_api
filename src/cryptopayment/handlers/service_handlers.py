import datetime

from fastapi import APIRouter, Request

from models import ChannelTg, User
from schemas import ServiceChannelID

from services.utils import check_token

service_router = APIRouter()


@service_router.get("/get_channels", tags=['service'])
async def get_channels(request: Request) -> dict:
    await check_token(request)
    return {'result': await ChannelTg.all()}


@service_router.post("/add_channel", tags=['service'])
async def add_channel(channel: ServiceChannelID, request: Request) -> dict[str: ChannelTg]:
    await check_token(request)

    return {'result': await ChannelTg.create(**channel.dict())}


@service_router.get("/get_expiration_data", tags=['service'])
async def get_expiration_data(request: Request) -> list:
    await check_token(request)
    current_date = datetime.datetime.utcnow()
    current_plus_3 = current_date + datetime.timedelta(days=3)

    data = await (
        User.filter(expired_at__gte=current_date)
            .filter(expired_at__lte=current_plus_3)
            .values('expired_at', 'telegram_id')
    )

    return data
