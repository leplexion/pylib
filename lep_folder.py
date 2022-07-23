import os
import pathlib


def folder_create(path:str):
    '''递归创建文件夹, 已存在不操作'''
    os.makedirs(path, exist_ok=True)

def folder_not_exist(path:str)->str:
    '''文件夹存在返回none, 否则返回错误信息'''
    if not os.path.exists(path):
        return 'path_not_exist'
    if not pathlib.Path(path).is_dir():
        return 'path_exist_but_not_dir'
    return None

def folder_exist(path:str)->bool:
    '''文件夹存在'''
    return os.path.exists(path) and pathlib.Path(path).is_dir()

