from fastapi import APIRouter, Response, Request, BackgroundTasks
from starlette import status

from models import Product, LicenseStatus, License
from schemas import ProductIn_Pydantic, SecondaryManagerData
from schemas.data_schemas import DataStructureProduct, DataStructureProductList
from datastructurepack import DataStructure

from services.exceptions import exception_unauthorized
from services.utils import check_token

product_router = APIRouter()


@product_router.post('/add_product', response_model=DataStructure, tags=['products', ])
async def add_product(product: ProductIn_Pydantic, response: Response, request: Request):
    await check_token(request)

    result = DataStructure()
    product = await Product.create(**product.dict())
    result.status = 200
    response.status_code = status.HTTP_201_CREATED
    result.success = True
    result.data = await ProductIn_Pydantic.from_tortoise_orm(product)
    return result.as_dict()


@product_router.get('/get_all_products', response_model=DataStructureProductList, tags=['products', ])
async def get_all_products(response: Response, request: Request):
    await check_token(request)

    result = DataStructure()
    result.status = 200
    result.success = True
    result.data = await Product.all()
    if not result.data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return result.as_dict()


@product_router.get('/get_product/{id}', response_model=DataStructureProduct, tags=['products', ])
async def get_product(id: int, response: Response, request: Request):
    await check_token(request)

    result = DataStructure()
    result.status = 200
    result.success = True
    result.data = await Product.filter(id=id).first()
    if not result.data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return result.as_dict()
