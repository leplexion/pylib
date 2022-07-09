import hashlib


def md5hex(str:str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()