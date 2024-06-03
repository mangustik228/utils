from datetime import datetime
from uuid import uuid4

from ._exceptions import ExcExpectedNamesArguments
from ._logger import get_logger


class BaseSaveManager:
    def __init__(self, base_path: str = "data", add_uuid: bool = False, compress: bool = False, debug: bool= False):
        '''
        Saver for files

        ```python 
        # Example for use (async version): 
        saver = AsyncSaveManager(base_path="example", compress=True)
        path = await saver.save_html("this is content", "seller_id", 4, 5)
        print(path) # "example/2024/05/29/22/seller_id_4_5.html.xz"

        # Example for use (sync version):
        saver = SyncSaveManager(add_uuid=True)
        path = saver.save_json({"hello":"world"}, 5, 3, daily)
        print(path) # "data/2024/05/29/22/5_3_daily.json"

        Parameters
        ----------
        base_path : str, optional
            Базовая папка в которой будут сохраняться все файлы, by default "data"
        add_uuid : bool, optional
            Возможно добавить uuid в конец файла, чтоб файлы были точно уникальными, by default False
        compress : bool, optional
            При включенной опции будет сжимать файлы с помощью lzma, by default False
        '''
        base_path = base_path.rstrip("/")
        self.base_path = base_path
        self.add_uuid = add_uuid
        self.compress = compress
        self.logger = get_logger(self.__class__.__name__, debug)

    @property
    def date_path(self):
        return datetime.now().strftime("/%Y/%m/%d/%H/")

    @property
    def folder_path(self):
        return self.base_path + self.date_path

    @property
    def uuid(self):
        if self.add_uuid:
            return "_" + str(uuid4()).split("-")[0]
        return ''

    def _get_json_file_name(self, names: tuple):
        path = self._get_name_from_name(names) + ".json"
        return f"{path}.xz" if self.compress else path

    def _get_html_file_name(self, names: tuple):
        path = self._get_name_from_name(names) + ".html"
        return f"{path}.xz" if self.compress else path

    def _get_name_from_name(self, names: tuple):
        if len(names) == 0:
            raise ExcExpectedNamesArguments
        return "_".join([str(n) for n in names]) + self.uuid
