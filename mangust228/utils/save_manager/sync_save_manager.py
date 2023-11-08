import tarfile
from .base_save_manager import BaseSaveManager


class SyncSaveManager(BaseSaveManager):
    def save_content(self, content: str, file_name: str) -> None:
        if self.files_in_folder >= self.max_files:
            self._update_current_folder()
        self.files_in_folder += 1

        path = self._get_path_to_file(file_name)

        if self.compression:
            self._save_xz(content, path)
        else:
            self._save_html(content, path)

    def _save_html(self, content: str, path: str):
        with open(path, "w") as file:
            file.write(content)

    def _save_xz(self, content: str, path: str):
        with tarfile.open(path, 'w:xz') as file:
            compressed_data = lzma.compress(content.encode())
            await file.write(compressed_data)
