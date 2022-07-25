import pathlib
import os
import sys
import __main__

def str2filename(s:str, maxch:int=127):
    '''将url的path转换为创建文件名可用的字符串, 空白或为空返回@符号'''
    divch = '@'
    replaces = {
        '/': divch,
        '\\': divch,
        '?': '[w]',
        '*': '[x]',
        '|': '[i]',
        '>': '[r]',
        '<': '[l]',
        '"': '[y]',
    }
    if not s: 
        return divch
    
    s = str(s)
    if not s.strip(): 
        return divch

    res = ''
    for ch in s:
        if replaces.__contains__(ch):
            res += replaces[ch]
        else:
            res += ch
    if len(res) > maxch:
        res = res[:maxch]

    return res

def working_dir(): 
    '''获取工作目录'''
    return str(pathlib.Path().parent.absolute())

def exec_path(): 
    '''执行器路径, 编译后则返回编译的文件'''  
    return sys.executable

def exec_dir(): 
    '''执行器的目录'''
    return str(pathlib.Path(sys.executable).parent.absolute())


def get_path_in_dir(path:str): 
    '''获取路径所在的上一层目录'''
    return str(pathlib.Path(path).parent.absolute())


def get_main_dir():
    '''获取 入口 文件所在目录'''
    if is_compiled(): return exec_dir()
    return str(pathlib.Path(__main__.__file__).parent.absolute())


def get_main_path():
    '''获取入口文件完整目录'''
    if is_compiled(): return exec_path()
    return str(pathlib.Path(__main__.__file__).absolute())


def abspath(path:str): 
    '''传入路径获取完整路径'''
    return str(os.path.abspath(path))


def get_name_noext(path:str)->str:
    '''获取没有路径的文件名'''
    if path == '' or path is None: return ''
    path = path.replace('\\', '/')
    if path[-1:] == '/': return ''
    if '/' in path:
        path = path.split('/')[-1]
    if '.' not in path: return path
    return '.'.join(path.split('.')[:-1])


def get_ext(path:str)->str:
    '''获取没有路径的文件名'''
    if path == '' or path is None: return ''
    path = path.replace('\\', '/')
    if path[-1:] == '/': return ''
    if '/' in path:
        path = path.split('/')[-1]
    if '.' not in path: return ''
    return path.split('.')[-1]


def is_file_ext(path:str, ext:str):
    return get_ext(path).lower() == ext.split('.')[-1].lower()


def path_exist(path:str)->bool:
    '''判断路径是否存在'''
    path = abspath(path)
    return pathlib.Path(path).exists()


def is_compiled(): 
    '''判断是否在编译的环境'''
    return getattr(sys, 'frozen', False)


def get_parent_dir(path:str): 
    '''获取上一级目录'''
    return pathlib.Path(path).parent.absolute()


def get_dir_list(dir:str='', mode:str='', recursion:bool=False, ensuredir:bool=True, ext:str=''):
    '''
        目录下所有的文件列表
        不用绝对路径则默认在 工作目录 下

        mode 可能的值:
            fname: 文件名
            fnoext: 不带后缀的文件名
            ffullpath: 文件完整路径

            dname: 文件夹名
            dfullpath: 文件夹完整路径

            bname: 两者都包含的仅名称, 递归模式下可能有重, 将去重
            bfullpath: 两者都包含的完整路径
    '''
    if dir == '': 
        dir = get_main_dir()
    else:
        dir = abspath(dir)
    
    if '/' in dir:
        div = '/'
    else:
        div = '\\'

    if ensuredir and (not pathlib.Path(dir).exists()):
        raise Exception(f'get_dir_list()查找的工作路径不存在{dir}')

    if not mode: 
        mode = 'fname'

    def modeget(res:list, cdir, dirls, filels):
        if mode == 'fname':
            if ext == '':
                res.extend(filels)
            else:
                res.extend(filter(lambda file: is_file_ext(file, ext), filels))

        elif mode == 'fnoext':
            if ext == '':
                res.extend([get_name_noext(f) for f in filels])
            else:
                res.extend([get_name_noext(f) for f in filter(lambda file: is_file_ext(file, ext), filels)])
                
        elif mode == 'ffullpath':
            # print(1)
            if ext == '':
                res.extend([(f'{cdir}{div}{f}') for f in filels])
            else:
                res.extend(filter(lambda path: is_file_ext(path, ext), [ f'{cdir}{div}{f}' for f in filels]))

        elif mode == 'dname':
            res.extend(dirls)
        elif mode == 'dfullpath':
            res.extend([(f'{cdir}{div}{d}') for d in dirls])
        elif mode == 'bname':
            res.extend(filels)
            res.extend(dirls)
        elif mode == 'bfullpath':
            res.extend([(f'{cdir}{div}{d}') for d in dirls])
            res.extend([(f'{cdir}{div}{f}') for f in filels])

    res = []
    for cdir, dirls, filels in os.walk(dir):
        if recursion:
            modeget(res, cdir, dirls, filels)
        elif (cdir == dir):
            modeget(res, cdir, dirls, filels)

    return list(dict.fromkeys(res))

if __name__ == '__main__':
    for key in get_dir_list(mode='fnoext', ensuredir=True, ext='py'):
        print(key)