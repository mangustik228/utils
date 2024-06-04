import pytest

from mangust228.utils.repo import AsyncBaseRepo, AsyncBaseRepoFactory
from tests.test_repo.utils import (Base, RoleModel, UserModel,
                                   session_maker, sync_engine)


class UserRepo(AsyncBaseRepo[UserModel]):
    model = UserModel

class RoleRepo(AsyncBaseRepo[RoleModel]):
    model = RoleModel

class MyFactory(AsyncBaseRepoFactory):
    session = session_maker
    user: UserRepo
    role: RoleRepo
    
@pytest.fixture
def db():
    Base.metadata.create_all(sync_engine)
    yield
    Base.metadata.drop_all(sync_engine)

@pytest.mark.asyncio(scope="session")
async def test_async_factory_add(db):
    async with MyFactory() as repo: 
        result = await repo.user.add_by_kwargs(name="Vasiliy")
        assert result.id == 1 

@pytest.mark.asyncio(scope="session")
async def test_async_factory_get(db):
    async with MyFactory() as repo:
        result = await repo.role.add_by_kwargs(name="admin")
        assert result.id == 1 
        
    async with MyFactory(commit=False) as repo: 
        role = await repo.role.get_one_or_none(id=1)
        assert role is not None 
        assert role.name == role.name
        assert isinstance(role, RoleModel)

@pytest.mark.asyncio(scope="session")
async def test_async_factory_emtpy_value(db):
    async with MyFactory(commit=False) as repo:
        result = await repo.role.get_one_or_none(id=5)
        assert result is None 
        
@pytest.mark.asyncio(scope="session")
async def test_async_factory_empty_list(db):
    async with MyFactory() as repo: 
        result = await repo.user.get_many()
        assert result == []

@pytest.mark.asyncio(scope="session")
async def test_async_factory_get_many_limit_and_offset(db):
    async with MyFactory() as repo: 
        for i in range(10):
            await repo.user.add_by_kwargs(name=f'Vasiliy-{i}', surname=f'Ovchinnikov-{i//3}')    
    
    async with MyFactory() as repo: 
        result = await repo.user.get_many()
        assert len(result) == 10 
    
    async with MyFactory(commit=False) as repo:
        result = await repo.user.get_many(surname="Ovchinnikov-1")
        assert len(result) == 3 
        assert result[0].name == "Vasiliy-3"
        
    async with MyFactory() as repo: 
        result = await repo.user.get_many(limit=5)
        assert len(result) == 5 
        assert result[-1].name == "Vasiliy-4"
    
    async with MyFactory() as repo: 
        result = await repo.user.get_many(limit=4, offset=8)
        assert len(result) == 2
        assert result[0].name == "Vasiliy-8"
        
    async with MyFactory() as repo: 
        result = await repo.user.get_many(offset=5)
        assert len(result) == 5 
        assert result[0].name == "Vasiliy-5"

@pytest.mark.asyncio(scope="session")
async def test_async_factory_count(db):
    async with MyFactory() as repo: 
        result = await repo.user.count()
        assert result == 0 
        await repo.user.add_by_kwargs(name="Vasiliy")
    
    async with MyFactory() as repo: 
        result = await repo.user.count()
        assert result == 1     
        
@pytest.mark.asyncio(scope="session")
async def test_async_factory_delete(db):
    async with MyFactory() as repo: 
        for i in ("admin","moderator","guest"):
            await repo.role.add_by_kwargs(name=i)
            await repo.role.add_by_kwargs(name=i)
    
    async with MyFactory() as repo: 
        await repo.role.delete(name="guest")
        await repo.role.delete(id=1)
        
    async with MyFactory() as repo: 
        count_admin = await repo.role.count(name="admin")
        assert count_admin == 1
        count_moderator = await repo.role.count(name="moderator")
        assert count_moderator == 2 
        count_total = await repo.role.count()
        assert count_total == 3 
        
@pytest.mark.asyncio(scope="session")
async def test_async_factory_update(db):
    async with MyFactory() as repo:
        user = await repo.user.add_by_kwargs(name="Kristina", surname="Kochi")
        user_id = user.id
        assert user_id == 1 
    
    async with MyFactory() as repo: 
        user = await repo.user.update_by_id(user_id, surname="Ovchinnikova")
        assert user is not None 
        assert user.id == 1 
    
    async with MyFactory() as repo: 
        user = await repo.user.get_one_or_none(id=user_id)
        assert user is not None 
        assert user.name == "Kristina"
        assert user.surname == "Ovchinnikova"
        
        
@pytest.mark.asyncio(scope="session")
async def test_async_factory_update_emtpy(db):
    async with MyFactory() as repo:
        result = await repo.user.update_by_id(id=5, name="world")
        assert result == None
        
        
@pytest.mark.asyncio(scope="session")
async def test_async_factory_add_by_model(db):
    async with MyFactory() as repo: 
        model = UserModel(name="Vasiliy", surname="Ovchinnikov")
        result = repo.user.add_by_model(model)
        assert result is None  
        
    
    async with MyFactory() as repo: 
        users = await repo.user.get_many(name="Vasiliy")
        assert len(users) == 1  