
import random

from ._browsers import Browsers
from ._engines import Engines
from ._oses import Oses


class UaRandom:
    ''' 
    Класс для получения рандомного user-agent
    Пример использования: 
    ```python

    UaRandom.web()
    >> "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Gecko/104 Firefox/104.0"

    UaRandom.web("chrome")
    >> ... 

    ```

    '''
    ...
    _web_browsers = ["chrome", "firefox", "safari"]

    @classmethod
    def web(cls, browser: str | None = None) -> str:
        if browser is None:
            browser = random.choice(cls._web_browsers)

        os_system = getattr(Oses, browser)
        version, engine = getattr(Engines, browser)
        browser_string = getattr(Browsers, browser)(version)

        result = "Mozilla/5.0 ("
        result += os_system
        if random.choice([True, False]):
            result += f"; rv:{version}"
        result += ") "
        result += engine
        result += f" {browser_string}"
        return result
