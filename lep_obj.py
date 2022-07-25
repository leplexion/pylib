
from inspect import signature




def objExistMethod(obj, methodname, argscount: int= None):
    '''查看对象是否存在方法'''
    if methodname not in dir(obj): 
        return f'对象不存在的方法:{methodname}'
    res = getattr(obj, methodname)
    if type(res).__name__ != 'method': 
        return f'对象字段{methodname}不是方法'
    sig = signature(res)
    if argscount and argscount != len(sig.parameters):
        return f'对象方法{methodname}不是参数数量不对实际参数数量{len(sig.parameters)}, 传入检查参数数量{argscount}'
    return None



if __name__ == '__main__':
    class A:
        def __init__(self) -> None:
            pass
        def abc(self, a):
            pass    
    a = A()
    abc = getattr(a, 'abc')
    abc(a, 'aa')
