from tokenize import PlainToken
import psutil
import os
import platform

def process_close(pid):
    '''通过pid关闭进程'''
    p = psutil.Process(pid)
    p.terminate()

def get_current_pid():
    '''获取本进程的pid'''
    return os.getpid()

def process_close_self():
    '''关闭本进程'''
    process_close(get_current_pid())

def getptrsize()->int:
    '''判断指针长度, 单位字节'''
    return int(platform.architecture()[0][:2])  // 8

def isptr32bit()->bool:
    '''判断本进程是32位程序'''
    return platform.architecture()[0][:2] == '32'

def isptr64bit()->bool:
    '''判断本进程是32位程序'''
    return platform.architecture()[0][:2] == '64'

if __name__ == '__main__':
    print(getptrsize())