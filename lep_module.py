from ast import Module
import sys

try:
    from .lep_path import get_name_noext, abspath, get_parent_dir
    from .lep_folder import folder_exist
except:
    from lep_path import get_name_noext, abspath, get_parent_dir
    from lep_folder import folder_exist

def sys_path_unshift(folder:str):
    '''sys.path列表元素单位为为模块读入位置的目录, 越往左(下标越小)查找优先级越高'''
    if not folder_exist(folder): 
        raise Exception('sysPathInsertFor()错误: 要添加至sys.path的文件夹不存在:' + dir)
    sys.path.insert(0, folder)

def sys_path_remove_first():
    '''sys.path列表元素单位为为模块读入位置的目录, 越往左(下标越小)查找优先级越高'''
    sys.path = sys.path[1:]

def module_exist(module_name:str)->bool:
    '''是否存在模块'''
    return sys.modules.__contains__(module_name)

def module_del_exist(module_name:str):
    '''删除模块, 在下次import时将重新载入, 但不删除现有的引用'''
    if sys.modules.__contains__(module_name):
        del sys.modules[module_name]

def import_py_once(path:str)->Module:
    '''从路径加载py模块, '''
    module = None
    path = abspath(path)
    module_name = get_name_noext(path)
    if sys.modules.__contains__(module_name):
        return sys.modules[module_name]
    else:
        return import_py(path)

def import_py(path:str, import_again:bool=True)->Module:
    '''从路径加载py模块, 返回模块, import_again: 是否重新载入(python模块将重新执行一遍)'''
    module = None
    path = abspath(path)
    pydir = get_parent_dir(path)
    sys_path_unshift(pydir)
    module_name = get_name_noext(path)
    try:
        if import_again:
            module_del_exist(module_name)
        module = __import__(module_name)
    except Exception as e:
        sys_path_remove_first()
        raise e
    sys_path_remove_first()
    return module

def import_py_ensure_attrs(path:str, *attrs:str, import_again:bool=True)->Module:
    '''重新载入py文件, 并确定模块中有特定的属性'''
    module = import_py(path, import_again=import_again)
    for attr in attrs:
        if not hasattr(module, attr):
            raise Exception(f'该python模块中不存属性[{attr}]:\n{path}')
    return module

def import_py_get_attrs(path:str, *attrs:str, import_again:bool=True)->tuple:
    if len(attrs) < 1:
        raise Exception('要获取的属性名称列表长度不得为0')
    module = import_py(path, import_again=import_again)
    res = []
    for attr in attrs:
        if not hasattr(module, attr):
            raise Exception(f'该python模块中不存属性[{attr}]:\n{path}')
        res.append(getattr(module, attr))
    return tuple(res)
    
if __name__ == '__main__':
    module1 = import_py_ensure_attrs('./Lep_Mongo.py', 'pymongo', import_again=False)
    module2 = import_py('./Lep_Mongo.py', import_again=False)
    print(module1 == module2)
    print(module1, module2)