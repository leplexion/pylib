
try:
    from .lep_path import get_ext, get_name_noext
    from .lep_file import fileread
    from .lep_yaml import yaml_load_file
    from .lep_module import import_py, import_py_get_attrs
except:
    from lep_path import get_ext, get_name_noext
    from lep_file import fileread
    from lep_yaml import yaml_load_file
    from lep_module import import_py, import_py_get_attrs

import json


# --------------------------------------------------------------------------------
def LoadHeaders(path:str):
    return HeaderLoader(path).headers

class HeaderLoader:
    '''使header从文件载入, 只导入一次, json, yaml, py中直接引入header 或 headers 值'''
    _map = {}
    def __init__(self, path:str) -> None:
        if HeaderLoader._map.__contains__(path):
            self.headers = HeaderLoader._map[path]
        else:
            ext = get_ext(path)
            if ext == 'py':
                HeaderLoader._map[path] = import_py_get_attrs(path, 'headers')[0]

            elif ext == 'json':
                HeaderLoader._map[path] = json.loads(fileread(path))

            elif ext == 'yaml':
                HeaderLoader._map[path] = yaml_load_file(path)

            else:
                raise Exception(f'不支持的格式:{ext}')

            if HeaderLoader._map.__contains__(path):
                self.headers = HeaderLoader._map[path]
    
if __name__ == '__main__':
    print(HeaderLoader('./Lep_Requests_Headers_Test.py').headers)
    print(HeaderLoader('./Lep_Requests_Headers_Test.py').headers)
    pass