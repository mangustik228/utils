import os
from mangust228.utils import SyncSaveManager, AsyncSaveManager
import pytest


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
    content = "world"
    saver.save_content(content, "world")
    assert os.path.exists(f"{folder_path}/2023/September/01/1/world.html.xz")
