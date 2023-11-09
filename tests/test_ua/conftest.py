import pytest


@pytest.fixture(params=[i for i in range(100)])
def repeat_100_times(request):
    return request.param
