from mangust228 import UaRandom


def test_validate_agents():
    for _ in range(10):
        UaRandom.web()

def test_uniques():
    user_agents = set()
    for _ in range(100):
        user_agents.add(UaRandom.web())
    assert len(user_agents) >= 96

def test_ua_chrome():
    for _ in range(50):
        ua = UaRandom.web("chrome")
        assert "Chrome" in ua 

def test_ua_safari():
    for _ in range(50):
        ua = UaRandom.web("safari") 
        assert ("Macintosh; Intel Mac OS X 10_15_7" in ua) or ("Macintosh; Intel Mac OS X 10.15" in ua)