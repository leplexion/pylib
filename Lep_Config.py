import yaml
from pathlib import Path
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from .lep_json import Json2FilePretty
import json

class CONFIG_KEY_ERROR(Exception): pass

class LepConfig:
    def __init__(self, file:str, model: dict) -> None:
        self.model = model
        self.conf = model
        self.file = file
        if Path(file).exists():
            with open(file, 'r', encoding='utf-8') as f:
                fileconf = yaml.load(f.read(), Loader)
                f.close()
                if fileconf is None:
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(yaml.dump(model))
                        f.close()
                else:
                    for key in fileconf:
                        if not model.__contains__(key):
                            print('配置文件中读取的键与模型不一致')
                            print(f'文件[{file}]')
                            print(json.dumps(self.conf, sort_keys=True, indent=4, separators=(',', ': ')))
                            print(f'model:')
                            print(json.dumps(model, sort_keys=True, indent=4, separators=(',', ': ')))
                            raise CONFIG_KEY_ERROR(f'配置文件中读取的键与模型不一致:{key}')
                    self.conf = fileconf
        else:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(yaml.dump(model))
                f.close()

    def save(self):
         with open(self.file, 'w', encoding='utf-8') as f:
            f.write(yaml.dump(self.conf))
            f.close()

    def get(self):
        return self.conf
        
    def setkey(self, key:str, val):
        if not self.conf.__contains__(key):
            raise CONFIG_KEY_ERROR(f'配置中不存在该键: {key}')
        self.conf[key] = val
        self.save()

    def set(self, newconf:dict):
        for key in newconf:
            if not self.model.__contains__(key):
                print('配置文件中读取的键与模型不一致')
                print(f'文件[{self.file}]')
                print(json.dumps(self.conf, sort_keys=True, indent=4, separators=(',', ': ')))
                print(f'model:')
                print(json.dumps(self.model, sort_keys=True, indent=4, separators=(',', ': ')))
                raise CONFIG_KEY_ERROR('配置文件中读取的键与模型不一致')
        for key in newconf:
            self.conf[key] = newconf[key]
        self.save()
    



if __name__ == '__main__':
    conf = LepConfig('a.yaml')
