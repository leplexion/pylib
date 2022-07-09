def filewrite(content:str, file:str, encoding = 'utf-8'):
    with open(file, 'w', encoding=encoding) as f:
        f.write(content)
        f.close()

def filewriteb(_bytes: bytes, file:str, encoding='utf-8'):
    a: str = ''
    if (type(_bytes).__name__ == 'str'):
        _bytes = _bytes.encode(encoding)
    with open(file, 'wb') as f:
        f.write(_bytes)
        f.close()

