import json
import lzma
from typing import Any

import aiofiles
import aiofiles.os as aos

from ._base import BaseSaveManager


class AsyncSaveManager(BaseSaveManager):
    '''Класс для сохранения файлов
    Пример использования: 
    ```python 
    saver = AsyncSaveManager()
    path = await saver.save_html(content, "seller_id", 2, "world")
    # >> "data/2020/05/15/12/seller_id_2_world.html" 
    '''

    async def _save_async_file(self, content: str, path: str):
        if not self.compress:
            async with aiofiles.open(path, "w") as fp:
                await fp.write(content)
        else:  # lzma
            compressed_data = lzma.compress(content.encode())
            async with aiofiles.open(path, "wb") as compress_fp:
                await compress_fp.write(compressed_data)

    async def save_json(self, data: dict, *names: Any) -> str:
        file_name = self._get_json_file_name(names)
        content = json.dumps(data, ensure_ascii=False)
        folder_path = self.folder_path
        await aos.makedirs(folder_path, exist_ok=True)
        path = folder_path + file_name
        await self._save_async_file(content, path)
        return path

    async def save_html(self, content, *names: Any) -> str:
        file_name = self._get_html_file_name(names)
        folder_path = self.folder_path
        await aos.makedirs(folder_path, exist_ok=True)
        path = folder_path + file_name
        await self._save_async_file(content, path)
        return path
