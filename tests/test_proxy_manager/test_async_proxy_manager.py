import httpx
import pytest
from pytest_httpx import HTTPXMock

from mangust228.proxy_manager import ProxySchema, AsyncProxyManager
from mangust228.proxy_manager._exceptions import ProxyManagerHttpException

mock_data_1 = {
    "id": 1, 
    "server": "example_server", 
    "port": 5000,
    "username": "example_username", 
    "password": "example_password"
    }

mock_data_2 = {
    "id": 2, 
    "server": "example_server_2", 
    "port": 5001,
    "username": "example_username_2", 
    "password": "example_password_2"
    }

mock_data_change_with_error = {
  "proxy_id": 1,
  "parsed_service_id": 2,
  "location_id": 1,
  "type_id": 1,
  "lock_time": 300
}

@pytest.mark.asyncio
async def test_async_get_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations/one?parsed_service=test&parsed_service_id=1&lock_time=5&location_id=1&type_id=1"
    mock_response = mock_data_1.copy()
    httpx_mock.add_response(200, url=api_url, json=mock_response)
    async with AsyncProxyManager(url=url) as pm:
        proxy = await pm.get()
        assert proxy.username == "example_username"

async def test_async_get_not_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations/one?parsed_service=test&parsed_service_id=1&lock_time=5&location_id=1&type_id=1"
    error_msg = {"detail":"Proxies exist, but none are available"}
    httpx_mock.add_response(404, url=api_url, json=error_msg)
    async with AsyncProxyManager(url=url) as pm:
        with pytest.raises(ProxyManagerHttpException) as exc_info:
            await pm.get()
    assert str(exc_info.value) == str(error_msg)

async def test_async_change_with_error_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations"
    httpx_mock.add_response(200, json=mock_data_2, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    async with AsyncProxyManager(url=url) as pm:
        proxy_2 = await pm.change_with_error(proxy_1, "test")
        assert isinstance(proxy_2, ProxySchema)
        assert proxy_1 != proxy_2
        
async def test_async_change_with_error_not_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations"
    error_msg = {"detail":"Proxies exist, but none are available"}
    httpx_mock.add_response(400, json=error_msg, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    async with AsyncProxyManager(url=url) as pm:
        with pytest.raises(ProxyManagerHttpException) as exc_info:
            await pm.change_with_error(proxy_1, "test")
    assert str(exc_info.value) == str(error_msg)

async def test_async_change_without_error_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations"
    httpx_mock.add_response(200, json=mock_data_2, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    async with AsyncProxyManager(url=url) as pm:
        proxy_2 = await pm.change_without_error(proxy_1)
        assert isinstance(proxy_2, ProxySchema)
        assert proxy_1 != proxy_2

async def test_async_change_without_error_not_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations"
    error_msg = {"detail":"Proxies exist, but none are available"}
    httpx_mock.add_response(400, json=error_msg, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    async with AsyncProxyManager(url=url) as pm:
        with pytest.raises(ProxyManagerHttpException) as exc_info:
            await pm.change_with_error(proxy_1, "test")
    assert str(exc_info.value) == str(error_msg)


async def test_async_free(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations/free/1"
    httpx_mock.add_response(200, json=mock_data_2, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    async with AsyncProxyManager(url=url) as pm:
        assert isinstance(proxy_1, ProxySchema)
        free_result = await pm.free(proxy_1)
        assert free_result is None
