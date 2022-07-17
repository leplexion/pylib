import json
import re
try:
    from .lep_time import get_now_acc_msec
    from .lep_path import get_dir_list
except:
    from lep_time import get_now_acc_msec
    from lep_path import get_dir_list

def Json2FilePretty(dic, dir:str)->str:
    path = re.sub('\\/+', '/', f'{dir}/{get_now_acc_msec()}.json')
    t = type(dic).__name__
    if t == 'dict' or t == 'list':
        t = json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': '))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(t)
            f.close()
        # print(f'Json2FilePretty()保存到{path}')
    elif t == 'str':
        t = json.loads(dic)
        t = json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': '))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(t)
            f.close()
        # print(f'Json2FilePretty()保存到{path}')
    else:
        raise Exception('该函数不支持的类型:', t)

    return path

def json2file(dic, dir:str)->None:
    path = re.sub('\\/+', '/', f'{dir}/{get_now_acc_msec()}.json')
    t = type(dic).__name__
    if t == 'dict' or t == 'list': 
        t = json.dumps(dic)
    elif t == 'str':
        t = json.dumps(json.loads(dic))
    else:
        raise Exception('该函数不支持的类型:', t)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
        f.close()
    return path

def jsonfromfile(file:str):
    with open(file, 'r', encoding='utf-8') as f:
        j = f.read()
        f.close()
    j = json.loads(j)
    return j

def json2filepretty(j:dict, file:str):
    with open(file, 'w', encoding='utf-8') as f:
        txt = json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))
        f.write(txt)
        f.close()

def jsonpretty(dic):
    t = type(dic).__name__
    if t == 'dict':
        return json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': '))
    elif t == 'str':
        t = json.loads(dic)
        return json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        raise Exception('该函数不支持的类型:', t)

def jsonloadfile(path:str):   # ->list
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()
        f.close()
    return json.loads(t)

def jsonloaddir(folder:str)->list:
    res: list = []
    for jsonfile in get_dir_list(folder, mode='ffullpath', ext='json'):
        with open(jsonfile, 'r', encoding='utf-8') as f:
            res.append(json.loads(f.read()))
            f.close()
    return res

def jsondumpfile(j:dict, file:str):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(j))
        f.close()

        