import re

def re_test(parttern:str, s:str)->bool:
    return bool(re.search(pattern=parttern, string=s))

def re_one(parttern:str, s:str)->str:
    res = re_all(parttern=parttern, s=s)
    return res[0] if res else None

def re_idx(parttern:str, s:str)->int:
    '''返回第一个匹配到的下标'''
    # return re.find()
    res = re_all_ex(parttern=parttern, s=s)
    if res.empty:
        return None
    else:
        return res.ls[0].start

def re_range(parttern:str, s:str)->tuple:
    '''返回第一个匹配到的下标范围[start:end]'''
    res = re_all_ex(parttern=parttern, s=s)
    if res.empty:
        return (None, None)
    else:
        item = res.ls[0]
        return (item.start, item.end)
    
def re_all(parttern:str, s:str)->list:
    '''返回匹配的字符串列表'''
    res = re.findall(pattern=parttern, string=s)
    return res if res else None

class ReAllExItem:
    def __init__(self, index:int, part:str, start:int, end:int, _len:int) -> None:
        self.index= index
        self.part = part
        self.start = start
        self.end = end
        self.len = _len

    def __str__(self) -> str:
        return f'part{self.index}=[{self.part}], start={self.start}, end={self.end}, len={self.len}'

class ReAllExResult:
    def __init__(self) -> None:
        self.ls = []
        self.len = 0
        self.empty = True

    def push(self, part:str, start:int, end:int, _len:int):
        self.ls.append(ReAllExItem(len(self.ls), part, start, end, _len))
        self.len+=1
        self.empty = False

    def __str__(self):
        return '\n'.join([str(item) for item in self.ls])

def re_all_ex(parttern:str, s:str)->ReAllExResult:
    '''返回匹配的所有下标'''
    result = re.finditer(pattern=parttern, string=s)
    if not result: return []
    res = ReAllExResult()
    for i in result:
        pos = i.span()
        start = pos[0]
        end = pos[1]
        part = s[start: end]
        res.push(part=part, start=start, end=end, _len=end-start)
    return res

if __name__ == '__main__':
    res = re_test('\d+', '123')
    res = re_idx('\d+', 'aas12346')
    print(res)