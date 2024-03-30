from sqlalchemy import select, insert, delete, update
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def create_object(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete_object_by_id(cls, object_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == object_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_object(cls, object_id: int, **fields):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == object_id).values(
                **fields
            ).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()
