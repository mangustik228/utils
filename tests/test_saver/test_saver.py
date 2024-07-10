import lzma
import os

import pytest
import shutil
from mangust228.saver import SyncSaveManager, AsyncSaveManager
from mangust228.saver._exceptions import ExcExpectedNamesArguments


def test_path_base():
    saver = SyncSaveManager()
    assert saver.folder_path == "data/2023/09/15/12/" 
    
def test_path_slash_in_end(): 
    saver = SyncSaveManager("hello/world/")
    assert saver.folder_path == "hello/world/2023/09/15/12/" 
    
def test_path_slash_in_start():
    saver = SyncSaveManager("/hello/world/")
    assert saver.folder_path == "/hello/world/2023/09/15/12/" 
    
    
def test_sync_json():
    saver = SyncSaveManager("tests/src/")
    data = {"hello":"world"}
    saver.save_json(data, "hello","world")
    assert os.path.exists("tests/src/2023/09/15/12/hello_world.json")
    shutil.rmtree("tests/src/2023/09/15/12/")

def test_sync_uuid_json():
    base_path = "tests/src/uuid/"
    shutil.rmtree(base_path)
    saver = SyncSaveManager(base_path, add_uuid=True, compress=True)
    data = {"hello":"world"}
    saver.save_json(data, "hello","second")
    files = os.listdir(f"{base_path}/2023/09/15/12/")
    assert len(files) == 1 
    assert files[0].startswith("hello_second_")
    assert files[0].endswith(".json.xz")
    
    
def test_sync_html():
    saver = SyncSaveManager("tests/src")
    saver.save_html("hello world", "this", 3, "seller")
    assert os.path.exists("tests/src/2023/09/15/12/this_3_seller.html")
    
    
def test_sync_html_emtpy_names_error():
    saver = SyncSaveManager("tests/src")
    with pytest.raises(ExcExpectedNamesArguments): 
        saver.save_html("hello world")
        
@pytest.mark.asyncio 
async def test_async_html_base():
    saver = AsyncSaveManager("tests/src")
    await saver.save_html("this is test message", "hello", "async", 2)
    assert os.path.exists("tests/src/2023/09/15/12/hello_async_2.html")

@pytest.mark.asyncio
async def test_async_html_correct_xz():
    saver = AsyncSaveManager("tests/src", compress=True)
    expect = "tests/src/2023/09/15/12/hello_async_3.html.xz"
    msg = "this is second test message"
    result = await saver.save_html(msg, "hello", "async", 3)
    assert expect == result 
    with open(expect, "rb") as fp: 
        compressed_content = fp.read()
        content = lzma.decompress(compressed_content).decode()
    assert content == msg
    
@pytest.mark.asyncio
async def test_async_json():
    saver = AsyncSaveManager("tests/src")
    expect = "tests/src/2023/09/15/12/test_async_json_5.json"
    result = await saver.save_json({"hello":"world"}, "test", "async", "json", 5)
    assert result == expect