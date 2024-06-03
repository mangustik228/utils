'''Class для проверки, а проходился ли этот файл или url. создает два файла: 
data/wrong.csv (Если вызвались ошибки)
data/success.csv (Если ошибок не было)

Пример использования: 

from parsed_manager import AsyncParsedManager as ParsedManager

await ParsedManager.wrong.add("url/path", reason) # Добавляет ошибочную запись
await ParsedManager.success.add("url/path") # Добавляет успешно спарсенную 

if ParsedManager.wrong.is_exist():
    pass # Сюда заходит если парсилось до этого.

'''



from .async_manager import AsyncParsedManager
from .sync_manager import SyncParsedManager