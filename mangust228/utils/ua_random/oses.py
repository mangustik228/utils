import random


TREE = {
    "chrome": [
        ("Windows NT 10.0; Win64; x64", .5),
        ("Windows NT 10.0", .3),
        ("Windows NT 6.1", .2),
        ("Macintosh; Intel Mac OS X 10_15_7", .2),
        ("X11; Ubuntu; Linux x86_64", .1),
        ("Windows NT 6.1; WOW64; Trident/7.0; AS", .3)
    ],
    "firefox": [
        ("Windows NT 10.0; Win64; x64", .3),
        ("Windows NT 10.0", .2),
        ("Windows NT 6.1", .3),
        ("X11; Ubuntu; Linux x86_64", .4),
        ("Windows NT 6.1; WOW64; Trident/7.0; AS", .3),
    ],
    "safari": [
        ("Macintosh; Intel Mac OS X 10_15_7", .5),
        ("Macintosh; Intel Mac OS X 10.15", .5)
    ]

}


class Oses:
    chrome_lst = [i[0] for i in TREE["chrome"]]
    chrome_weight = [i[1] for i in TREE["chrome"]]

    firefox_lst = [i[0] for i in TREE["firefox"]]
    firefox_weight = [i[1] for i in TREE["firefox"]]

    safari_lst = [i[0] for i in TREE["safari"]]
    safari_weight = [i[1] for i in TREE["safari"]]

    @classmethod
    @property
    def chrome(cls):
        return random.choices(cls.chrome_lst, weights=cls.chrome_weight)[0]

    @classmethod
    @property
    def firefox(cls):
        return random.choices(cls.firefox_lst, weights=cls.firefox_weight)[0]

    @classmethod
    @property
    def safari(cls):
        return random.choices(cls.safari_lst, weights=cls.safari_weight)[0]
