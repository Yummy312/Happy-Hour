from app.companies.dao import CompanyDAO
import pytest
from app.companies.models import Company


@pytest.mark.parametrize('company_id, name, exists', [
    (1, "PepsiCo", True),
    (2, "Coca-Cola", True),
    (224, "Some Company", False)
])
async def test_find_by_id(company_id, name, exists):
    company = await CompanyDAO.find_by_id(company_id)

    if exists:
        assert company.id == company_id
        assert company.name == name
        assert company
    else:
        assert not company


@pytest.mark.parametrize('name, location', [
    ("PepsiCo", "Purchase, New York\n"),
    ("Coca-Cola", "Georgia, Atlanta.\n"),
    ("Example name", 'Florida')
])
async def test_find_one_or_none(name, location):
    company = await CompanyDAO.find_one_or_none(name=name, location=location)
    if company:
        assert company.location == location
        assert company.name == name
    else:
        assert not company


async def test_find_all():
    companies = await CompanyDAO.find_all()
    assert len(companies) > 0
    assert isinstance(companies, list)
    for company in companies:
        assert isinstance(company, Company)


@pytest.mark.parametrize('name, description, location, hours_of_operation', [
    ("Jack Daniel Inc", "Company", "Greece", "from 9 to 14:00"),

])
async def test_create_object(name, description, location, hours_of_operation):
    await CompanyDAO.create_object(
        name=name,
        description=description,
        location=location,
        hours_of_operation=hours_of_operation
    )
    found_company = await CompanyDAO.find_one_or_none(name=name)
    if found_company:
        assert found_company.name == name
        assert found_company.description == description


async def test_delete_object_by_id():
    await CompanyDAO.delete_object_by_id(4)
    exists_company = await CompanyDAO.find_by_id(4)
    assert exists_company is None


@pytest.mark.parametrize('company_id, name, description, location, hours_of_operation', [
    (1, "Fanta", "Company is an American", "USA", "from 7:00 to 19:00"),

])
async def test_update_object(company_id, name, description, location, hours_of_operation):
    await CompanyDAO.update_object(
        object_id=company_id,
        name=name,
        description=description,
        location=location,
        hours_of_operation=hours_of_operation
    )
    updated_company = await CompanyDAO.find_by_id(company_id)
    if updated_company:
        assert updated_company.name == name
        assert updated_company.description == description
        assert updated_company.location == location
        assert updated_company.id == company_id
    else:
        assert not updated_company
