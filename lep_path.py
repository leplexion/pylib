import pathlib
import os
import sys
import __main__

# 获取工作路径
def working_dir(): return pathlib.Path().parent.absolute()

# 执行器路径, 编译后则返回编译的文件
def exec_path(): return sys.executable

# 执行器的目录
def exec_dir(): return pathlib.Path(sys.executable).parent.absolute()

# 获取路径所在的上一层目录
def get_path_in_dir(path:str): return pathlib.Path(path).parent.absolute()

# 获取 入口 文件所在目录, 
def get_main_dir():
    if is_compiled(): return exec_dir()
    return pathlib.Path(__main__.__file__).parent.absolute()

# 获取入口文件完整目录
def get_main_path():
    if is_compiled(): return exec_path()
    return pathlib.Path(__main__.__file__).absolute()

# 传入路径获取完整路径
def abspath(path:str): return os.path.abspath(path)

def get_name_noext(path:str):
    path = abspath(path)

# 判断是否在编译的环境
def is_compiled(): return getattr(sys, 'frozen', False)

# 获取上一级目录
def get_parent_dir(path:str): return pathlib.Path(path).parent.absolute()

if __name__ == '__main__':
    # print('是否已编译: ', is_compiled())
    print(get_path_in_dir('c:\\a\\b'))
