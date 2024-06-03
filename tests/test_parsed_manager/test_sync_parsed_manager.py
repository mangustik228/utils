import os

from mangust228.utils.parsed_manager import SyncParsedManager
from mangust228.utils.parsed_manager.sync_manager import (
    _SuccessSyncFileDesciptor, _WrongSyncFileDesciptor)


def test_sync_parsed_manager():
    path = "tests/parsed_manager/wrong/wrong.csv"
    SyncParsedManager.wrong = _WrongSyncFileDesciptor(path, ["path","exc"])
    SyncParsedManager.wrong.add("hello_world_1", "test")
    assert SyncParsedManager.wrong.is_exist("hello_world_1")
    os.remove(path)
    
    
def test_sync_parsed_manager_parsed():
    path = "tests/parsed_manager/success/success.csv"
    SyncParsedManager.success = _SuccessSyncFileDesciptor(path, ["path"])
    SyncParsedManager.success.add("hello_world_2")
    assert SyncParsedManager.success.is_exist("hello_world_2")
    os.remove(path)
    
def test_sync_parsed_manager_parsed_not_exist():
    path = "tests/parsed_manager/success/success.csv"
    SyncParsedManager.success = _SuccessSyncFileDesciptor(path, ["path"])
    SyncParsedManager.success.add("hello_world_2")
    assert not SyncParsedManager.success.is_exist("wrong_value")
    os.remove(path)

def test_sync_parsed_manager_parsed_wrong_few_rows():
    path = "tests/parsed_manager/wrong/wrong.csv"
    SyncParsedManager.wrong = _WrongSyncFileDesciptor(path, ["path","exc"])
    SyncParsedManager.wrong.add("hello_world_1", "test")
    SyncParsedManager.wrong.add("hello_world_2", "test")
    SyncParsedManager.wrong.add("hello_world_3", "test")
    SyncParsedManager.wrong.add("hello_world_4", "test")
    SyncParsedManager.wrong.add("hello_world_4", "test")
    with open(path, "r") as fp:
        data = set(f.strip().split(",")[0] for f in fp.readlines()[1:])
        
    assert SyncParsedManager.wrong._data == data
    os.remove(path)