from pydantic import BaseModel

from schemas import Product_Pydantic, User_Pydantic, PaymentResult, WalletIn_Pydantic


class DataStructure(BaseModel):
    pass


class DataStructureProductList(DataStructure):
    data: list[Product_Pydantic] = None


class DataStructureProduct(DataStructure):
    data: Product_Pydantic = None


class DataStructureUser(DataStructure):
    data: User_Pydantic = None


class DataStructurePaymentResult(DataStructure):
    data: PaymentResult = None


class DataStructureWallet(DataStructure):
    data: WalletIn_Pydantic = None

