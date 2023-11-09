from mangust228.utils import UaRandom
from user_agents import parse


user_agents = set()
for _ in range(100):
    user_agent = UaRandom.web()
    if user_agent in user_agents:
        print(user_agent)
    user_agents.add(UaRandom.web())
# assert len(user_agents) >= 99
