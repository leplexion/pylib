import urllib
try:
    from .lep_path import str2filename
except Exception as e:
    from lep_path import str2filename

urlpath2FileName = str2filename


def urlClearQuery(path:str):
    '''删除 # 和 ? 后面的内容'''
    if not path:
        return ''

    if path[0] == '?' or path[0] == '#':
        return ''

    if '?' in path:
        path = path.split('?')[0]

    if '#' in path:
        path = path.split('#')[0]
        
    return path
    


def encodeUriComponent(url:str, safe:str='/'):
    return urllib.parse.quote(url, safe=safe)
    
def decodeUriComponent():
    # todo
    pass

if __name__ == '__main__':
    print(encodeUriComponent('大阪府'))
