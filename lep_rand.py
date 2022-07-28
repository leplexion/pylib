import random


def randint(start:int, end:int)->str:
    '''包括end值'''
    return random.randint(start, end)

def randintzfill(length: int)->str:
    '''length=5 可能输出 01015 99999 00001'''
    return str(randint(0, int('9' * length))).zfill(length)
