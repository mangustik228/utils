import httpx
import pytest
from pytest_httpx import HTTPXMock

from mangust228.proxy import ProxySchema, SyncProxyManager
from mangust228.proxy._exceptions import ProxyManagerHttpException

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


def test_get_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations/one?parsed_service=test&parsed_service_id=1&lock_time=5&location_id=1&type_id=1"
    mock_response = mock_data_1.copy()
    httpx_mock.add_response(200, url=api_url, json=mock_response)
    with SyncProxyManager(url=url) as pm:
        proxy = pm.get()
        assert proxy.username == "example_username"

def test_get_not_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations/one?parsed_service=test&parsed_service_id=1&lock_time=5&location_id=1&type_id=1"
    error_msg = {"detail":"Proxies exist, but none are available"}
    httpx_mock.add_response(404, url=api_url, json=error_msg)
    with SyncProxyManager(url=url) as pm:
        with pytest.raises(ProxyManagerHttpException) as exc_info:
            pm.get()
    assert str(exc_info.value) == str(error_msg)

def test_change_with_error_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations"
    httpx_mock.add_response(200, json=mock_data_2, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    with SyncProxyManager(url=url) as pm:
        proxy_2 = pm.change_with_error(proxy_1, "test")
        assert isinstance(proxy_2, ProxySchema)
        assert proxy_1 != proxy_2
        
def test_change_with_error_not_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations"
    error_msg = {"detail":"Proxies exist, but none are available"}
    httpx_mock.add_response(400, json=error_msg, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    with SyncProxyManager(url=url) as pm:
        with pytest.raises(ProxyManagerHttpException) as exc_info:
            pm.change_with_error(proxy_1, "test")
    assert str(exc_info.value) == str(error_msg)

def test_change_without_error_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations"
    httpx_mock.add_response(200, json=mock_data_2, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    with SyncProxyManager(url=url) as pm:
        proxy_2 = pm.change_without_error(proxy_1)
        assert isinstance(proxy_2, ProxySchema)
        assert proxy_1 != proxy_2

def test_change_without_error_not_200(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations"
    error_msg = {"detail":"Proxies exist, but none are available"}
    httpx_mock.add_response(400, json=error_msg, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    with SyncProxyManager(url=url) as pm:
        with pytest.raises(ProxyManagerHttpException) as exc_info:
            pm.change_with_error(proxy_1, "test")
    assert str(exc_info.value) == str(error_msg)


def test_free(httpx_mock: HTTPXMock):
    url = "http://example.com"
    api_url = "http://example.com/proxies/rotations/free/1"
    httpx_mock.add_response(200, json=mock_data_2, url=api_url)
    proxy_1 = ProxySchema(**mock_data_1)
    with SyncProxyManager(url=url) as pm:
        assert isinstance(proxy_1, ProxySchema)
        free_result = pm.free(proxy_1)
        assert free_result is None
