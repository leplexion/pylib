import urllib


def encodeUriComponent(url:str, safe:str='/'):
    return urllib.parse.quote(url, safe=safe)
    
def decodeUriComponent():
    # todo
    pass
