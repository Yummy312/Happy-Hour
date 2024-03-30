from typing import List
from fastapi import APIRouter
from app.companies.schemas import CompanyBase, CompanyRetrieve
from app.companies.dao import CompanyDAO
from app.exceptions import *

router = APIRouter(
    prefix='/companies',
    tags=['companies']
)


@router.get('', response_model=List[CompanyRetrieve])
async def get_all_companies():
    return await CompanyDAO.find_all()


@router.get('/{company_id}', response_model=CompanyRetrieve)
async def get_company(company_id: int):
    company = await CompanyDAO.find_by_id(company_id)
    if not company:
        raise ProductNotExists
    return company


@router.post('', response_model=CompanyRetrieve)
async def create_company(company: CompanyBase):
    existing_company = await CompanyDAO.find_all(name=company.name)
    if existing_company:
        raise CompanyExists
    new_company = await CompanyDAO.create_object(
        **company.model_dump()
    )
    return new_company


@router.delete('/{company_id}')
async def delete_company(company_id: int):
    company = await CompanyDAO.find_by_id(company_id)
    if not company:
        raise CompanyNotExists

    await CompanyDAO.delete_object_by_id(company_id)
    return {"message": "Product deleted successfully"}


@router.put('/{company_id}', response_model=CompanyBase)
async def update_company(company_id: int, company: CompanyBase):
    company_found = await CompanyDAO.find_by_id(company_id)
    if not company_found:
        raise CompanyNotExists

    updated_company = await CompanyDAO.update_object(
        object_id=company_id,
        **company.model_dump()
    )
    return updated_company
