import os
from datetime import datetime
from mangust228.exceptions import EmptyFileName
from functools import reduce


class BaseSaveManager:
    allowed_formats = {".html", ".json"}

    def __init__(self,
                 base_path: str = "data",
                 compression: bool = False,
                 max_files: int = 5000,
                 file_format: str = ".html",
                 sep: str = "_"):
        '''
        class for save contents in folders

        Parameters
        ----------
        base_path : str, optional
            base path, where will save files, by default "data"
        compression : bool, optional
            if True - files will save in with .xz compression, by default False
        max_files : int, optional
            How many files can be in ones folder, by default 5000
        file_format : str, optional
            Format of files, allowed values: {.json, .html}, by default ".html"
        sep : str, optional
            Separator for separate params in file_name, by default "_"
        '''
        self.compression = compression
        self.sep = sep
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

    def _get_file_name_from_args(self, *file_name: list[str]):
        if not file_name:
            raise EmptyFileName(
                "Failed to receive arguments for filename designation.")

        result = ""
        for name in file_name:
            if isinstance(name, str):
                name = name.replace(
                    "https://", "").replace("/", "__").replace(".", "___")
            if isinstance(name, int):
                name = str(name)
            result += f"{self.sep if result else ''}{name}"

        return result
