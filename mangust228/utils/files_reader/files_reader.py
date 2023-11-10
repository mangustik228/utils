import os
from collections import namedtuple
from typing import Generator
import lzma


File = namedtuple("File", ["path", "params", "content"])


def get_files_paths(base_path: str, file_format: str, sep: str = "_", return_content=False) -> Generator[File, None, None]:
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
    return_content: bool
        Можно возвращать сразу контент, если указан архив ".xz", то вернет уже разжатый


    Yields
    ------
    Generator[File, None, None]
        _description_
    '''

    def get_content(fp: str):
        if not return_content:
            return
        if file_format[-2:] == "xz":
            with open(fp, mode="rb") as file:
                bytes_data = file.read()
            content = lzma.decompress(bytes_data)
            return content.decode("utf-8")
        with open(fp, "r") as file:
            content = file.read()
        return content

    def get_info(fp: str):
        if fp[-2:] == "xz":
            params = fp.replace(".xz", "")
        params = fp.split("/")[-1].split(".")[0]
        params = params.replace("___", ".").replace("__", "/")
        result_params = []
        for param in params.split(sep):
            if param.isdigit():
                result_params.append(int(param))
            else:
                result_params.append(param)

        content = get_content(fp)

        return File(path=fp, params=result_params, content=content)

    for path in os.listdir(base_path):
        current_path = f"{base_path}/{path}"
        if os.path.isdir(current_path):
            yield from get_files_paths(current_path, file_format, sep, return_content)
        elif current_path[-len(file_format):] == file_format:
            yield get_info(current_path)
