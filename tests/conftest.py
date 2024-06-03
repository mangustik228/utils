import pytest
import os
import logging 



@pytest.fixture(scope="session", autouse=True)
def disable_logging():
    logging.disable(50)

os.environ["MODE"] = "TEST"
