from mangust228.utils import SyncProxyManager, ProxySchema


def test_get():
    with SyncProxyManager() as pm:
        proxy = pm.get()
        assert str(proxy).startswith("proxy-")


def test_change_with_error():
    with SyncProxyManager() as pm:
        proxy_1 = pm.get()
        assert isinstance(proxy_1, ProxySchema)
        proxy_2 = pm.change_with_error(proxy_1, "test")
        assert isinstance(proxy_2, ProxySchema)
        assert proxy_1 != proxy_2


def test_change_without_error():
    with SyncProxyManager() as pm:
        proxy_1 = pm.get()
        assert isinstance(proxy_1, ProxySchema)
        proxy_2 = pm.change_without_error(proxy_1)
        assert isinstance(proxy_2, ProxySchema)
        assert proxy_1 != proxy_2


def test_free():
    with SyncProxyManager() as pm:
        proxy_1 = pm.get()
        assert isinstance(proxy_1, ProxySchema)
        free_result = pm.free(proxy_1)
        assert free_result is None 