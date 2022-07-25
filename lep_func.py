from inspect import signature

def get_args_count(fn):
    '''获取函数参数数量'''
    sig = signature(fn)
    return len(sig.parameters)



