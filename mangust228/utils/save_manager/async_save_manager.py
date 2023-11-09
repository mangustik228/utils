from .base_save_manager import BaseSaveManager
import aiofiles
import lzma


class AsyncSaveManager(BaseSaveManager):
    async def save_content(self, content: str, file_name: str) -> None:
        if self.files_in_folder >= self.max_files:
            self._update_current_folder()
        self.files_in_folder += 1

        path = self._get_path_to_file(file_name)
        if self.compression:
            await self._save_xz(content, path)
        else:
            await self._save_html(content, path)

    async def _save_xz(self, content: str, path: str):
        bytes_content = content.encode("utf-8")
        compressed_data = lzma.compress(bytes_content)
        async with aiofiles.open(path, 'wb') as file:
            file.write(compressed_data)

    async def _save_html(self, content: str, path: str):
        async with aiofiles.open(path, "w") as file:
            await file.write(content)
