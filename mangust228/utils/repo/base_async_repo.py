from typing import Any, Sequence
from sqlalchemy import delete, insert, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

class AsyncBaseRepo[M: DeclarativeBase]:
    '''How to use: 
    ```python 

    class MyRepo(AsyncBaseRepo[MyModel]):
        model = MyAlchemyModel
    ```
    '''
    model: type[M]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, **kwargs: Any) -> M:
        '''add item and return model.id
        (BASE MUST HAVE id: Mapped[int])
        ```python
        await factory.my_repo.add(my_model)
        # >> 1
        '''
        stmt = insert(self.model)\
            .values(**kwargs)\
            .returning(self.model)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, **by_filter: Any) -> None:
        '''delete values by_filter
        ```python
        await factory.my_repo.delete(id=5)
        ```
        '''
        stmt = delete(self.model).filter_by(**by_filter)
        await self.session.execute(stmt)

    async def update_by_id(self, id: int, **new_values: Any) -> None:
        '''update values by_filter
        ```python 
        # update name to NEW_NAME where model.id = 5 
        await factory.my_repo.update({"name":"NEW_NAME"}, id=5)
        ```
        '''
        stmt = update(self.model)\
            .values(**new_values)\
            .where(self.model.id == id) # type: ignore 
        await self.session.execute(stmt)

    async def get_one_or_none(self, **by_filter: Any) -> M | None:
        '''
        return one PydanticModel or None by filters
        ```python
        await factory.my_repo.get_one_or_none(id=3) 
        # >> MyModel(id=3, name="Ivan", surname="Ivanov")
        await factory.my_repo.get_one_or_none(name="NONAME") 
        # >> None
        ```
        p.s. BE CAREFUL, if you send nothing or filter with many conditions:
        method will return just first item from datebase.
        Probably you need to use `factory.my_repo.get_many()`
        ```python
        await factory.my_repo.get_one_or_none(surname=None) 
        # >> MyModel(id=5, name="Ivan", surname=None)

        await factory.my_repo.get_many(surname=None) 
        # >> [MyModel(id=5, name="Ivan", surname=None), MyModel(id=6, name="Sergey", surname=None), ...]
        ```    
        '''
        stmt = select(self.model).filter_by(**by_filter)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_many(self,
                       limit: int | None = None,
                       offset: int | None = None,
                       **by_filter: Any) -> Sequence[M]:
        '''return list of items
        ```python
        await factory.my_repo.get_one(surname=None) 
        # >> MyModel(id=5, name="Ivan", surname=None)

        await factory.my_repo.get_many(surname=None) 
        # >> [MyModel(id=5, name="Ivan", surname=None), MyModel(id=6, name="Sergey", surname=None), ...]
        ```    
        '''
        stmt = select(self.model)\
            .filter_by(**by_filter)\
            .limit(limit)\
            .offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def count(self, **filter_by) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.scalar_one()