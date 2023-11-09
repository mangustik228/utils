import os


def get_files_paths(base_path: str, file_format: str, sep: str = "_"):
    '''
    Возвращает генератор кортежей: 
    Второй элемент - путь 
    Третий и последующие - параметры которые были переданы при сохранении

    Parameters
    ----------
    base_path : str
        Базовая папка в которой искать файлы
    file_format : str
        Какой формат файлов искать
    sep : str, optional
        Разделитель для параметров, by default "_"
    '''

    def get_info(fp: str):
        params = fp.split("/")[-1].split(".")[0]
        params = params.replace("___", ".").replace("__", "/")
        return fp, *params.split(sep)

    for path in os.listdir(base_path):
        current_path = f"{base_path}/{path}"
        if os.path.isdir(current_path):
            yield from get_files(current_path, file_format)
        elif current_path[-len(file_format):] == file_format:
            yield get_info(current_path)
