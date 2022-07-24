from tokenize import PlainToken
import psutil
import os
import platform
import subprocess

def command(cmd:str):
    '''code, data, err = command()'''
    p = subprocess.Popen('ping 127.0.0.1', stdout=subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    return p.returncode,  stdoutdata, stderrdata

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
    '''判断指针长度, 单位bit'''
    return int(platform.architecture()[0][:2])

def is32ptr()->bool:
    '''判断本进程是32位程序'''
    return platform.architecture()[0] == '32bit'

def is64ptr()->bool:
    '''判断本进程是32位程序'''
    return platform.architecture()[0] == '64bit'

if __name__ == '__main__':
    print(getptrsize())