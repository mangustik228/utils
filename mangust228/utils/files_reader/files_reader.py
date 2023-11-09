import os
from collections import namedtuple
from typing import Generator


File = namedtuple("File", ["path", "params"])


def get_files_paths(base_path: str, file_format: str, sep: str = "_") -> Generator[File, None, None]:
    '''
    Функция для итерации по файлам с вложенной древовидной структурой.

    Parameters
    ----------
    base_path : str
        Путь к каталогу в котором искать файлы с нужным расширением
    file_format : str
        расширение файлов, которые будут возвращены
    sep : str, optional
        Используемый разделитель параметров в наименовании файла,, by default "_"

    Yields
    ------
    Generator[File, None, None]
        _description_
    '''

    def get_info(fp: str, sep: str):
        params = fp.split("/")[-1].split(".")[0]
        params = params.replace("___", ".").replace("__", "/")
        result_params = []
        for param in params.split(sep):
            if param.isdigit():
                result_params.append(int(param))
            else:
                result_params.append(param)
        return File(path=fp, params=result_params)

    for path in os.listdir(base_path):
        current_path = f"{base_path}/{path}"
        if os.path.isdir(current_path):
            yield from get_files_paths(current_path, file_format, sep)
        elif current_path[-len(file_format):] == file_format:
            yield get_info(current_path, sep)
