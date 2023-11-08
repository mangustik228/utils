import pytest
import os

os.environ["MODE"] = "TEST"


# class _NameSpace:
#     file_path = 'tests/src/test_ids'
#     debug = True


# @pytest.fixture(autouse=True)
# def mock_get_namespace(mocker):
#     mocker.patch('app.config.arg_parser.get_namespace',
#                  return_value=_NameSpace())
