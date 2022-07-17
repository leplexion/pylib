import os, codecs, encodings
_debug = 0

def oneinstr(s:str, *subs:str)->bool:
    '''subs中有一项在s中'''
    for sub in subs:
        if sub in s:
            return True
    return False

def cut_text(text:str,le:int)->list:
    '''切割字符串到数组'''
    # some_string="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return [text[y-le:y] for y in range(le, len(text)+le,le)]

def listcodecs():
    '''输出python所有可用的encoding, 见本地文件 "lep_str_py可用的encoding.html", 见[ https://docs.python.org/3.9/library/codecs.html#standard-encodings ]'''
    names = []
    for filename in os.listdir(encodings.__path__[0]):
        if filename[-3:] != '.py':
            continue
        name = filename[:-3]
        # Check whether we've found a true codec
        try:
            codecs.lookup(name)
        except LookupError:
            # Codec not found
            continue
        except Exception as reason:
            # Probably an error from importing the codec; still it's
            # a valid code name
            if _debug:
                print('* problem importing codec %r: %s' % \
                    (name, reason))
        names.append(name)
    return names

if __name__ == '__main__':
    print(listcodecs())
