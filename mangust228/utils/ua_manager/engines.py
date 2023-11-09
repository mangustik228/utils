import random


class Engines:
    @classmethod
    @property
    def chrome(cls):
        version = random.randint(99, 122)
        return version, f"AppleWebKit/537.{random.randint(11, 75)} (KHTML, like Gecko)"

    @classmethod
    @property
    def safari(cls):
        version = random.randint(10, 15)
        return version, f"AppleWebKit/{random.randint(601, 605)}/{random.randint(1,8)}/{random.randint(1,50)} (KHTML, like Gecko)"

    @classmethod
    @property
    def firefox(cls):
        version = random.randint(99, 120)
        if random.choice([True, False]):
            return version, "Gecko/20100101"
        return version, f"Gecko/{version}"
