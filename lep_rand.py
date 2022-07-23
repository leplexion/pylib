import random


def randint(start:int, end:int)->str:
    '''包括end值'''
    return random.randint(start, end)

def randintzfill(length: int)->str:
    ''''''
    return str(randint(0, int('9' * length))).zfill(length)
