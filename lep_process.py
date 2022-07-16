import psutil
import os


def process_close(pid):
    p = psutil.Process(pid)
    p.terminate()

def get_current_pid():
    return os.getpid()

def process_close_self():
    process_close(get_current_pid())