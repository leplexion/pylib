import urllib


def urlpath2FileName(path:str, ignore_query:bool=True):
    '''将url的path转换为创建文件名可用的字符串'''
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
    if not path:
        return divch
    res = ''
    for ch in path:
        if replaces.__contains__(ch):
            res += replaces[ch]
        else:
            res += ch
    return res

def encodeUriComponent(url:str, safe:str='/'):
    return urllib.parse.quote(url, safe=safe)
    
def decodeUriComponent():
    # todo
    pass

