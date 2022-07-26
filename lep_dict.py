def dict_has(d:dict, *keys:str)->bool:
    '''递归查找dict中的键'''
    if not type(d) is dict:
        raise Exception('dict_has函数只用于判断dict类型数据')
    for k in keys:
        if not type(d) is dict:
            return False
        if k in d:
            d = d[k]
        else:
            return False
    return True


if __name__ == '__main__':
    a = {
        'a': {
            'b': 123
        }
    }
    print( dict_has(a, 'a', 'b', 'c') )