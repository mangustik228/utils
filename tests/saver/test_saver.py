import os
from mangust228.utils import SyncSaveManager, AsyncSaveManager
import pytest
from mangust228.exceptions import EmptyFileName
import lzma


def test_saver_base(folder_path):
    SyncSaveManager(folder_path)
    assert os.path.exists(folder_path), "folder not exist"
    assert os.path.exists(f"{folder_path}/2023/September/01/1")


def test_saver_exception(folder_path):
    with pytest.raises(ValueError):
        SyncSaveManager(folder_path, file_format=".xa")


def test_save_date(folder_path):
    saver = SyncSaveManager(folder_path, max_files=50)
    content = "hello"
    for i in range(101):
        saver.save_content(content, f"file_{i}")
    assert len(os.listdir(f"{folder_path}/2023/September/01/1/")) == 50
    assert len(os.listdir(f"{folder_path}/2023/September/01")) == 3


def test_save_xz(folder_path):
    saver = SyncSaveManager(folder_path, compression=True)
    content = "hello world"
    saver.save_content(content, "world")
    file_path = f"{folder_path}/2023/September/01/1/world.html.xz"
    assert os.path.exists(file_path)

    with open(file_path, "rb") as file:
        bytes_data = file.read()
        read_content = lzma.decompress(bytes_data)
    assert content == read_content.decode("utf-8")


def test_empty_name(folder_path):
    saver = SyncSaveManager(folder_path)
    content = "hello world"
    with pytest.raises(EmptyFileName):
        saver.save_content(content)


def test_with_exist_folder(folder_path):
    for i in range(1, 50):
        os.makedirs(f"{folder_path}/2023/September/01/{i}")
    saver = SyncSaveManager(folder_path)
    for i in range(15):
        saver.save_content("hello world", i)
    assert len(os.listdir(f"{folder_path}/2023/September/01/49")) == 15
