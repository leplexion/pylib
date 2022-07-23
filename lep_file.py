import os
import pathlib

def filewrite(content:str, file:str, encoding = 'utf-8'):
    with open(file, 'w', encoding=encoding) as f:
        f.write(content)
        f.close()

def filewriteb(_bytes: bytes, file:str, encoding='utf-8'):
    a: str = ''
    if (type(_bytes).__name__ == 'str'):
        _bytes = _bytes.encode(encoding)
    with open(file, 'wb') as f:
        f.write(_bytes)
        f.close()

def fileread(path:str, encoding='utf-8'):
    res = None
    with open(path, 'r', encoding=encoding) as f:
        res = f.read()
        f.close()
    return res

def file_exist(path:str)->bool:
    return os.path.exists(path) and pathlib.Path(path).is_dir()

def file_not_exist(path:str)->str:
    '''文件夹存在返回none, 否则返回错误信息'''
    if not os.path.exists(path):
        return 'path_not_exist'
    if not pathlib.Path(path).is_dir():
        return 'path_exist_but_not_dir'
    return None
