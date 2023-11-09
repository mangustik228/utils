import os
from datetime import datetime


class BaseSaveManager:
    allowed_formats = {".html", ".json"}

    def __init__(self,
                 base_path: str = "data",
                 compression: bool = False,
                 max_files: int = 5000,
                 file_format: str = ".html"):
        self.compression = compression
        self.max_files = max_files
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        self.today_path = self._get_today_path()
        self.files_in_folder = None
        if file_format not in self.allowed_formats:
            raise ValueError(
                f"format to Saver must be equal: {self.allowed_formats}")
        self.format = file_format
        self._get_current_folder()

    def _get_today_path(self):
        today = datetime.today().strftime("%Y/%B/%d")
        path = f"{self.base_path}/" + today
        self._create_folder(path)
        return path

    @property
    def full_folder_path(self):
        return f"{self.today_path}/{self.current_folder_in_day}"

    def _get_current_folder(self):
        folders = [int(i) for i in os.listdir(self.today_path)]
        if folders:
            folders += [0]
        current_folder_in_day = max(*folders) if folders else 1
        self.current_folder_in_day = current_folder_in_day
        self._create_folder(self.full_folder_path)
        files = os.listdir(self.full_folder_path)
        if len(files) >= self.max_files:
            self._update_current_folder()
        else:
            self.files_in_folder = len(files)

    def _create_folder(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    def _update_current_folder(self):
        self.current_folder_in_day += 1
        self.files_in_folder = 0
        self._create_folder(self.full_folder_path)

    def _get_path_to_file(self, file_name: int):
        path = f"{self.full_folder_path}/{file_name}{self.format}"
        return path + ".xz" if self.compression else path
