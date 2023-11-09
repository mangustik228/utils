import pytest
import os
import shutil
from freezegun import freeze_time


@pytest.fixture()
def folder_path():
    fp = "tests/src/test_data/"
    if os.path.exists(fp):
        shutil.rmtree(fp)
    yield fp
    shutil.rmtree(fp)


@pytest.fixture(scope="session", autouse=True)
def change_date():
    fixed_date = "2023-09-01 12:00:00"
    with freeze_time(fixed_date):
        yield
