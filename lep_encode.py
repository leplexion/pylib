import base64
try:
    from .lep_file import file_read_raw
except:
    from lep_file import file_read_raw

def str2b64raw(src:str, encoding='utf-8'):
    '''字符串转base64'''
    if type(src) is not str: raise Exception('str2b64raw仅支持str类型参数')
    raw = src.encode(encoding=encoding)
    return base64.b64encode(raw)

def str2b64(src:str, encoding='utf-8'):
    if type(src) is not str: raise Exception('str2b64仅支持str类型参数')
    return str2b64raw(src, encoding).decode('utf-8')

def raw2b64raw(raw:bytes):
    if type(raw) is not bytes: raise Exception('bytes2b64raw仅支持bytes类型参数')
    return base64.b64encode(raw)

def raw2b64(raw:bytes):
    if type(raw) is not bytes: raise Exception('bytes2b64仅支持bytes类型参数')
    return base64.b64encode(raw).decode('utf-8')

def file2b64raw(path:str):
    raw = file_read_raw(path)
    return raw2b64raw(raw)

def file2b64(path:str):
    raw = file_read_raw(path)
    return raw2b64(raw)



if __name__ == '__main__':
    res = file2b64('C:\\Users\\DY-I7\\Desktop\\abc.jpg')
    print(res)
    pass




