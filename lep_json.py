import json
import re
from .lep_time import get_now_acc_msec

def Json2FilePretty(dic, dir:str)->None:
    path = re.sub('\\/+', '/', f'{dir}/{get_now_acc_msec()}.json')
    t = type(dic).__name__
    if t == 'dict':
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


