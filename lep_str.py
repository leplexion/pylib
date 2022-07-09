
def oneinstr(s:str, *subs:str)->bool:
    for sub in subs:
        if sub in s:
            return True
    return False