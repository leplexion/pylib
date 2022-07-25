from .lep_path import get_ext, get_name_noext
from .lep_file import fileread
from .lep_yaml import yaml_load_file
import json


class HeaderLoader:
    '''使header从文件载入, 只导入一次, json, yaml, py中直接引入header 或 headers 值'''
    _map = {}
    def __init__(self, path:str, load_once:bool=True) -> None:
        if not load_once:

            ext = get_ext(path)
            if ext == 'py':
                pyname = get_name_noext(path)

            elif ext == 'json':
                HeaderLoader._map[path] = json.loads(fileread(path))

            elif ext == 'yaml':
                HeaderLoader._map[path] = yaml_load_file(path)

            else:
                raise Exception(f'不支持的格式:{ext}')

        if HeaderLoader._map.__contains__(path):
            self.headers = HeaderLoader._map[path]
    