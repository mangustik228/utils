import requests 
from mangust228.utils import SyncProxyManager

import httpx

def test_schema_correct_req_conn():
    with SyncProxyManager() as pm: 
        proxy = pm.get()
    response = requests.get("http://httpbin.org/ip", proxies=proxy.req_conn)
    response_data = response.json()
    assert proxy.server == response_data["origin"]
    
    
def test_schema_correct_httpx():
    with SyncProxyManager() as pm: 
        proxy = pm.get()
    response = httpx.get("http://httpbin.org/ip", proxy=proxy.httpx_conn)
    response_data = response.json()
    assert proxy.server == response_data["origin"]