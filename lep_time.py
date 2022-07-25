import time as Time

def get_now_acc_msec()->int: 
    '''# 毫秒级时间戳, acc=Accuracy=精度, 同javascript: new Date().getTime(), 如: 1657084042511'''
    return round(Time.time()*1000)

def get_now_acc_sec()->int: 
    '''# 秒级时间戳, acc=Accuracy=精度, 如: c'''
    return round(Time.time())

def get_now_origin()->float:  
    '''# 得到当前时间戳, 如: 1657083246.6974413'''
    return Time.time()

def get_now_struct()->Time.struct_time: 
    '''# 得到时间结构体, 如: time.struct_time(tm_year=2022, tm_mon=7, tm_mday=6, tm_hour=12, tm_min=56, tm_sec=39, tm_wday=2, tm_yday=187, tm_isdst=0)'''
    return Time.localtime()

def get_now_asc()->str: 
    '''# 得到时间字符串, 如: Wed Jul  6 12:57:56 2022'''    
    return Time.asctime( Time.localtime() )

def get_now_format(formatstr:str=None)->str: 
    '''# 得到时间字符串, 如: 2022-07-06 13:02:37'''
    if formatstr is None: formatstr = "%Y-%m-%d %H:%M:%S"
    return Time.strftime(formatstr, Time.localtime()) 

def time_format(time, formatstr:str): 
    '''# 格式化时间'''
    if type(time) == Time.struct_time:
        return Time.strftime(formatstr,time)
    return Time.strftime(formatstr, time_2_struct(time))

def time_2_struct(time):
    '''# 时间戳转 time.struct_time 类型'''
    tname = type(time).__name__
    if tname == 'int':
        l = len(str(time))
        if l == 13: # 毫秒级时间戳
            return Time.localtime(time / 1000)
        else:   # 秒级时间戳
            return Time.localtime(time)
    elif tname == 'float':
        return Time.localtime(time)
    elif tname == 'str':
        if '.' in time:
            return Time.localtime(float(time))
        l = len(time)
        if l == 13: # 毫秒级时间戳
            return Time.localtime(time / 1000)
        else:
            return Time.localtime(time)
    elif type(time) == Time.struct_time:
        return time
    
    else:
        raise Exception('错误的输入')
    
def time_format_help():
    '''# 格式化时间的帮助'''
    time = get_now_origin()
    print('时间戳 如:', time)
    time = Time.localtime(time)
    print('格式化 如:', "%Y-%m-%d %H:%M:%S", ',输出: ',Time.strftime("%Y-%m-%d %H:%M:%S", time))
    print(
        ' [%y] 2位年份:', Time.strftime("%y", time), '\n',
        '[%Y] 4位年份:', Time.strftime("%Y", time), '\n',
        '[%m] 2位月份:', Time.strftime("%m", time), '\n',
        '[%d] 2位日期:', Time.strftime("%d", time), '\n',
        '[%H] 2位 24小时制:', Time.strftime("%H", time), '\n',
        '[%I] 2位 12小时制:', Time.strftime("%I", time), '\n',
        '[%M] 2位分钟:', Time.strftime("%M", time), '\n',
        '[%S] 2位秒数:', Time.strftime("%S", time), '\n',
        '[%a] 英文星期缩写:', Time.strftime("%a", time), '\n',
        '[%A] 英文星期:', Time.strftime("%A", time), '\n',
        '[%b] 英文月份缩写:', Time.strftime("%b", time), '\n',
        '[%B] 英文月份:', Time.strftime("%B", time), '\n',
        '[%c] 格式化:', Time.strftime("%c", time), '\n',
        '[%p] 输出 am/pm (早上/下午):', Time.strftime("%p", time), '\n',
        '[%j] 一年中天数:', Time.strftime("%j", time), '\n',
        '[%U] 一年中星期数(周天起):', Time.strftime("%U", time), '\n',
        '[%W] 一年中星期数(周一起):', Time.strftime("%W", time), '\n',
        '[%w] 一周中星期数:', Time.strftime("%w", time), '\n',
        '[%x] 本地日期:', Time.strftime("%x", time), '\n',
        '[%X] 本地时间:', Time.strftime("%X", time), '\n',
        '[%Z] 当前时区:', Time.strftime("%Z", time), '\n',
        '[%%] 输出%百分号原来字符:', Time.strftime("%%", time), '\n',
    )

if __name__ == '__main__':
    # print( get_now_acc_msec() )
    # print( get_now_acc_sec() )
    # print( get_now_origin() )
    # print( get_now_struct() )
    # print( get_now_asc() )
    # print( get_now_format() )
    time_format_help()
