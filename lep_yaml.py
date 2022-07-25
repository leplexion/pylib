'''
pip install yaml
pip install pyyaml
'''

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def yaml_load(yamlstr:str)->dict:
    '''从字符串读取yaml到dict'''
    return yaml.load(yamlstr, Loader)
    
def yaml_dump(_map:dict):
    '''将dict转为yaml字符串'''
    return yaml.dump(_map, Dumper)

def yaml_load_file(file:str, encoding:str='utf-8')->dict:
    '''从文件读取yaml'''
    with open(file, 'r', encoding=encoding) as f:
        res = yaml.load(f.read())
        f.close()
    return res

def yaml_dump_file(_map:dict, file:str, encoding:str='utf-8')->str:
    '''将dict写入到文件并返回yaml字符串'''
    with open(file, 'w', encoding=encoding) as f:
        res = yaml.dump(_map, Dumper)
        f.write(res)
        f.close()
    return res



