import datetime
from typing import Type

from tortoise import ConfigurationError, fields, models
from enum import Enum


class Statuses(Enum):
    newbie: str = "newbie"
    member: str = "member"
    ex_member: str = "ex_member"
    admin: str = "admin"


class EnumField(fields.CharField):
    """
    An example extension to CharField that serializes Enums
    to and from a str representation in the DB.
    """

    def __init__(self, enum_type: Type[Enum], **kwargs):
        super().__init__(**kwargs)
        if not issubclass(enum_type, Enum):
            raise ConfigurationError("{} is not a subclass of Enum!".format(enum_type))
        self._enum_type = enum_type

    def to_db_value(self, value: Enum, instance) -> str:
        return value.value

    def to_python_value(self, value: str) -> Enum:
        try:
            return self._enum_type(value)
        except Exception:
            raise ValueError(
                "Database value {} does not exist on Enum {}.".format(value, self._enum_type)
            )


class User(models.Model):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, description="Telegram id")
    nick_name = fields.CharField(default="", max_length=50, description="Nickname name")
    created_at = fields.DatetimeField(auto_now_add=True, description="Create date")
    updated_at = fields.DatetimeField(auto_now=True, description="Create date")
    expired_at = fields.DatetimeField(auto_now_add=True, description="Expired date")
    status = EnumField(
        default=Statuses.newbie, enum_type=Statuses, max_length=50, description="Nickname name"
    )
    description = fields.TextField(default="", max_length=1500, description="Description")

    class PydanticMeta:
        table_description = "users"

    def save(self, *args, **kwargs):
        if not self.expired_at:
            self.expired_at = datetime.datetime.utcnow()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.nick_name


class Wallet(models.Model):
    id = fields.BigIntField(pk=True)
    wallet_id = fields.BigIntField(description="Wallet id")
    name = fields.CharField(max_length=50, unique=True, description="Wallet name")
    passphrase = fields.CharField(max_length=200, description="Wallet passphrase")
    address = fields.CharField(max_length=100, unique=True, description="Wallet address")
    main_network = fields.CharField(max_length=50, description="Wallet main_network")
    main_balance = fields.DecimalField(
        max_digits=20, decimal_places=2, description="Wallet balance"
    )
    main_balance_str = fields.CharField(max_length=50, description="Wallet balance string")
    user = fields.ForeignKeyField("models.User", related_name="wallets", on_delete=fields.RESTRICT)

    class Meta:
        table_description = "wallets"

    class PydanticMeta:
        exclude = ("id", "passphrase", "user")

    def __str__(self):
        return self.name


class Product(models.Model):
    """"""
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=50, description="Product name")
    price = fields.BigIntField(default=0, description="Product price in USD")
    filename = fields.CharField(max_length=100, description="Product file name")
    task_name = fields.CharField(default="", max_length=100, description="Product task name")
    description = fields.TextField(default="", max_length=1500, description="Description")

    class Meta:
        table_description = "products"

    def __str__(self):
        return self.name


class License(models.Model):
    """"""
    id = fields.BigIntField(pk=True)
    license = fields.CharField(max_length=100, description="License")
    product = fields.ForeignKeyField(
        "models.Product", related_name="licenses", on_delete=fields.CASCADE
    )
    user = fields.ForeignKeyField("models.User", related_name="licenses", on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True, description="Create date")
    expired_at = fields.DatetimeField(auto_now_add=True, description="Expired date")
    description = fields.TextField(default="", max_length=1500, description="Description")

    class Meta:
        table_description = "licenses"

    @classmethod
    def check_license(cls, license_key):
        return bool(License.exists(license_key=license_key))

    def __str__(self):
        return self.license


class LicenseStatus(models.Model):
    """"""
    id = fields.BigIntField(pk=True)
    license = fields.ForeignKeyField(
        'models.License',
        related_name='licenses_status',
        on_delete=fields.CASCADE
    )
    status = fields.IntField(default=-1)
    created_at = fields.DatetimeField(auto_now=True, description="Create date")

    class Meta:
        db_table = 'licenses_statuses'


class Service(models.Model):
    """"""
    id = fields.BigIntField(pk=True)
    frequency_of = fields.IntField(default=10, description='Chat check frequency')
    member_price = fields.IntField(default=10, description='Price for member')
    newbie_price = fields.IntField(default=100, description='Price for newbie')
    main_wallet = fields.CharField(max_length=100, description="Main wallet address")

    class Meta:
        db_table = 'services'


class ChannelTg(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100, default="", description='Chat name')
    chat_id = fields.BigIntField(description='Chat id')

    class Meta:
        db_table = 'channels'
