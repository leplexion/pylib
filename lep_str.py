
def oneinstr(s:str, *subs:str)->bool:
    for sub in subs:
        if sub in s:
            return True
    return False

def cut_text(text:str,le:int):
    # some_string="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return [text[y-le:y] for y in range(le, len(text)+le,le)]

if __name__ == '__main__':
    print(cut_text('', 5))