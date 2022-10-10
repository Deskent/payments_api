from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from models import User, Wallet, Product, License, LicenseStatus
from models.models import ChannelTg, Service
from pydantic import BaseModel


class SecondaryManagerData(BaseModel):
    check_status_id: int
    headers: dict
    product_data: list[dict]
    requests_count: int
    proxy_login: str
    proxy_password: str
    sale_time: str
    currency: str


class LicenseKey(BaseModel):
    license_key: str


class CheckStatus(LicenseKey):
    check_status_id: int


class ConfirmLicense(BaseModel):
    check_status_id: int
    telegram_id: int


class AddLicense(LicenseKey):
    telegram_id: int
    product_id: int


User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
WalletIn_Pydantic = pydantic_model_creator(Wallet, name="WalletIn", exclude_readonly=True)
WalletData_Pydantic = pydantic_model_creator(
    Wallet,
    name="WalletData",
    exclude=("id", "passphrase")
)
Product_Pydantic = pydantic_model_creator(Product, name="Product")
ProductIn_Pydantic = pydantic_model_creator(
    Product,
    name="ProductIn",
    exclude=('id',)
)

License_Pydantic = pydantic_model_creator(License, name="License")
License_Status_Pydantic = pydantic_model_creator(LicenseStatus, name="LicenseStatus")

License_Pydantic_List = pydantic_queryset_creator(
    License,
    name="License",
    include=("product__name", "product.description", "product.price")
)


class UserTelegramID(BaseModel):
    """
    telegram_id: int
    """
    telegram_id: int = 0


class UserCreate(UserTelegramID):
    """
    telegram_id: int

    nick_name: str
    """
    nick_name: str = ''


class CheckPayment(BaseModel):
    """
    telegram_id: int

    price_ltc: str
    """
    telegram_id: int = 0
    price_ltc: str = ''


class PaymentResult(BaseModel):
    """
    balance_before: str

    balance_after: str

    """
    balance_before: str = ''
    balance_after: str = ''


class ServiceChannelID(BaseModel):
    """
    name: str

    chat_id: int
    """
    name: str = ''
    chat_id: int = 0


class Deploy(BaseModel):
    repository: str
    stage: str
    version: str
