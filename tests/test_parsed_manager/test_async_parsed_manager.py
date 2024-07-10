# import os

# import pytest

# from mangust228.utils.parsed_manager import AsyncParsedManager
# from mangust228.utils.parsed_manager.async_manager import (
#     _SuccessAsyncFileDesciptor, _WrongAsyncFileDesciptor)


# @pytest.mark.asyncio
# async def test_parsed_manager():
#     path = "tests/parsed_manager/wrong/wrong.csv"
#     AsyncParsedManager.wrong = _WrongAsyncFileDesciptor(path, ["path","exc"])
#     await AsyncParsedManager.wrong.add("hello_world_1", "test")
#     assert AsyncParsedManager.wrong.is_exist("hello_world_1")
#     os.remove(path)
    
    
# @pytest.mark.asyncio
# async def test_parsed_manager_parsed():
#     path = "tests/parsed_manager/success/success.csv"
#     AsyncParsedManager.success = _SuccessAsyncFileDesciptor(path, ["path"])
#     await AsyncParsedManager.success.add("hello_world_2")
#     assert AsyncParsedManager.success.is_exist("hello_world_2")
#     os.remove(path)
    
# @pytest.mark.asyncio
# async def test_parsed_manager_parsed_not_exist():
#     path = "tests/parsed_manager/success/success.csv"
#     AsyncParsedManager.success = _SuccessAsyncFileDesciptor(path, ["path"])
#     await AsyncParsedManager.success.add("hello_world_2")
#     assert not AsyncParsedManager.success.is_exist("wrong_value")
#     os.remove(path)

# @pytest.mark.asyncio
# async def test_parsed_manager_parsed_wrong_few_rows():
#     path = "tests/parsed_manager/wrong/wrong.csv"
#     AsyncParsedManager.wrong = _WrongAsyncFileDesciptor(path, ["path","exc"])
#     await AsyncParsedManager.wrong.add("hello_world_1", "test")
#     await AsyncParsedManager.wrong.add("hello_world_2", "test")
#     await AsyncParsedManager.wrong.add("hello_world_3", "test")
#     await AsyncParsedManager.wrong.add("hello_world_4", "test")
#     await AsyncParsedManager.wrong.add("hello_world_4", "test")
#     with open(path, "r") as fp:
#         data = set(f.strip().split(",")[0] for f in fp.readlines()[1:])
        
#     assert AsyncParsedManager.wrong._data == data
#     os.remove(path)