import traceback
import json
def print_f(any):
    t = type(any).__name__

    if t=='str':
        print('-' * 30)
        print(any)
        print('-' * 30)
        print(f'输出内容为[字符串],长度{len(any)}')

    elif t=='list':
        print('-' * 30)
        print(json.dumps(any, sort_keys=True, indent=4, separators=(',', ': ')))
        print('-' * 30)
        print(f'输出内容为[列表],长度{len(any)}')

    elif t=='dict':
        any:dict = any
        print(json.dumps(any, sort_keys=True, indent=4, separators=(',', ': ')))
        print(f'输出内容为[字典],长度{len(any)}')    
    else:
        print_t(any)


def print_t(any):
    print('-' * 30)
    print('* 类型输出')
    print('-' * 30)
    print(f'{">> name".ljust(20)}>> method')
    props:list = dir(any)
    for prop in props:
        print(f'{prop.ljust(20)}{type(eval(f"any.{prop}")).__name__}')
    print(f'类型: {type(any).__name__}')
    print('-' * 30)


def print_e(e:Exception):
    print('-' * 30)
    print('* 异常输出')
    print('-' * 30)
    print('* 调用栈:')
    print(traceback.format_exc())
    print('-' * 30)
    print('* 错误消息:')
    print('\n'.join([f'[{i}]{e.args[i]}' for i in range(0, len(e.args))]))
    print('-' * 30)
    print(f'* 错误类型: {type(e).__name__}')
    print('-' * 30)


if __name__ == '__main__':
    # try:
    #     raise Exception('你好啊', '世界')
    # except Exception as e:
    #     print_e(e)

    print_f({'a': 123})