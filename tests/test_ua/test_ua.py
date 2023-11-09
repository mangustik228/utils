from user_agents import parse
from mangust228 import UaRandom
import pytest


def test_validate_agents():
    for _ in range(100):
        parse(UaRandom.web())


def test_chrome():
    for _ in range(100):
        ua = parse(UaRandom.web("chrome"))
        assert ua.browser.family == "Chrome"


def test_pc():
    for _ in range(100):
        ua = parse(UaRandom.web())
        assert str(ua)[:2] == "PC"


def test_uniques():
    user_agents = set()
    for _ in range(100):
        user_agents.add(UaRandom.web())
    assert len(user_agents) >= 96
