import asyncio
import json

import httpx
import pytest
from sqlalchemy import insert
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.companies.models import Company
from app.main import app
from app.products.models import Product
from fastapi.testclient import TestClient
from httpx import AsyncClient


# Флаг autouse=True сообщает python автоматически использовать фикстуру
@pytest.fixture(scope='session', autouse=True)
# Подготовка БД
async def prepare_database():
    # Первое- это самое важнно убедиться что режим сейчас TEST
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        # Создаем все таблицы, которые аккумулированы в Base
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model_name: str):
        # Так как мы находимся в корневой папке
        with open(f"app/tests/mock_{model_name}.json", encoding='utf-8') as file:
            return json.load(file)

    companies = open_mock_json('companies')
    products = open_mock_json('products')

    # Вставляем все данные в Алхимию, для этого нам нужен async_session_maker
    async with async_session_maker() as session:
        add_companies = insert(Company).values(companies)
        add_products = insert(Product).values(products)

        await session.execute(add_companies)
        await session.execute(add_products)
        await session.commit()


# Взято из документации к pytest-asyncio
@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.get_event_loop_policy()


@pytest.fixture(scope="function")
async def async_client():
    transport = httpx.ASGITransport(app=app)

    # В Asynclient мы передаем наше приложение app
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
