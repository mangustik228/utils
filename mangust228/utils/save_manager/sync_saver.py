import os
from typing import Any
from ._base import BaseSaveManager
import json
import lzma 
from ._exceptions import ExcExpectedNamesArguments

class SyncSaveManager(BaseSaveManager):
    def _save_sync_file(self, content: str, path: str):
        if not self.compress: 
            with open(path, "w") as fp:
                fp.write(content)
        else: # lzma 
            compressed_data = lzma.compress(content.encode())
            with open(path, "wb") as compress_fp: 
                compress_fp.write(compressed_data)
    
    def save_json(self, data: dict, *names: Any):
        file_name = self._get_json_file_name(names)
        folder_path = self.folder_path
        os.makedirs(folder_path, exist_ok=True)
        path = folder_path + file_name
        content = json.dumps(data, ensure_ascii=False)
        self._save_sync_file(content, path)
        return path 
    
    def save_html(self, content: str, *names: Any):
        file_name = self._get_html_file_name(names)
        folder_path = self.folder_path
        os.makedirs(folder_path, exist_ok=True)
        path = folder_path + file_name
        self._save_sync_file(content, path)
        return path 