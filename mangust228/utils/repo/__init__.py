'''
**description:** Module to easy make standard repositories with CRUD operations.

Example to use: 
```python 
from mangust228.utils.repo import AsyncBaseRepo, AsyncBaseRepoFactory

# Look for inherits in class! It's important to correct hinting
class UserRepo(AsyncBaseRepo[MyModel]):
    model = MyModel
    
class Repository(AsyncBaseRepoFactory):
    # CAUTION. Use only annotation
    user: UserRepo 
    another_repo: AnotherRepo


async with Repository() as repo: 
    user = await repo.user.add(name="Ivan", surname="Ivanov")
    user_id = user.id 
    await repo.user.count(surname="Ivanov")
    await repo.user.update(user_id, name="Sergey")
    await repo.user.get_one_or_none(surname="Ivanov") 
    ... 
    
'''


from .base_async_repo import AsyncBaseRepo
from .factory_repo import AsyncBaseRepoFactory
