import lzma

from .base_save_manager import BaseSaveManager


class SyncSaveManager(BaseSaveManager):
    def save_content(self, content: str, *file_name) -> None:
        '''
        *file_name - аргументы которые будут включены в названия файла. можно использовать url
        '''
        fp = self._get_file_name_from_args(*file_name)

        if self.files_in_folder >= self.max_files:
            self._update_current_folder()
        self.files_in_folder += 1

        path = self._get_path_to_file(fp)

        if self.compression:
            self._save_xz(content, path)
        else:
            self._save_html(content, path)

    def _save_html(self, content: str, path: str):
        with open(path, "w") as file:
            file.write(content)

    def _save_xz(self, content: str, path: str):
        bytes_content = content.encode("utf-8")
        compressed_data = lzma.compress(bytes_content)
        with open(path, "wb") as file:
            file.write(compressed_data)
