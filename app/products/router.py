from typing import List
from fastapi import APIRouter
from app.exceptions import CompanyNotExists, ProductNotExists, CompanyByIdNotExists
from app.companies.dao import CompanyDAO
from app.products.schemas import ProductCreate, ProductBase, ProductRetrieve, ProductDetail
from app.products.dao import ProductDAO

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('', response_model=List[ProductRetrieve])
async def get_products():
    return await ProductDAO.find_all()


@router.get('/{product_id}', response_model=ProductDetail)
async def get_product(product_id: int):
    product = await ProductDAO.find_by_id(product_id)
    if not product:
        raise ProductNotExists
    return product


@router.post('')
async def create_product(product: ProductCreate):
    existing_company = await CompanyDAO.find_by_id(product.company_id)
    if not existing_company:
        raise CompanyByIdNotExists

    new_product = await ProductDAO.create_object(
        **product.model_dump()
    )
    return new_product


@router.delete('/{product_id}')
async def delete_product(product_id: int):
    product = await ProductDAO.find_by_id(product_id)
    if not product:
        raise ProductNotExists
    await ProductDAO.delete_object_by_id(product_id)
    return {"message": "Product deleted successfully"}


@router.put('/{product_id}', response_model=ProductBase)
async def update_product(product_id: int, product: ProductBase):
    product_found = await ProductDAO.find_by_id(product_id)
    if not product_found:
        raise ProductNotExists

    updated_product = await ProductDAO.update_object(
        object_id=product_id,
        **product.model_dump()
    )
    return updated_product
