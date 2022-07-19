import ctypes
from ctypes import c_int, c_uint, c_void_p, c_wchar_p, _SimpleCData, create_string_buffer, pointer, cast, sizeof, string_at
import json
import platform
import __main__, sys, pathlib
from time import sleep

def is32ptr()->bool:
    '''判断本进程是32位程序'''
    return platform.architecture()[0] == '32bit'

def get_main_dir():
    '''获取 入口 文件所在目录'''
    if getattr(sys, 'frozen', False): return sys.executable
    return str(pathlib.Path(__main__.__file__).parent.absolute())

def getptrnum(ptr, ctype:_SimpleCData):
    '''
        # 获取数字类型指针的
        getptrnum(buff.ptr, c_int)
    '''
    return ctype.from_address(ptr).value
    
def setptrnum(ptr, ctype:_SimpleCData, val):
    '''
        # 设置数字类型指针的值, ctype 为 类型, 非实例化对象
        setptrnum(buff.ptr, c_int, 567)
    '''
    ctype.from_address(ptr).value = val

def getptrstr(ptr, size:int, encoding:str):
    '''
        # 获取指针的指向的字符串
        b = Lep_Buffer.create_from_str('你好世界')
        print(getptrstr(b.ptr, b.size, 'utf-8'))
    '''
    return string_at(ptr, size).decode(encoding)

def getptr(buff:_SimpleCData):
    '''
        # 获取已实例化的 ctype 的指针
        i = c_int(0)
        p = getbuffptr(i)
        print(getptrnum(i, c_int))
    '''
    return cast(pointer(buff), c_void_p).value

def getptrhex(buff:_SimpleCData):
    '''
        # 获取已实例化的 ctype 的指针, 返回十六进制字符串
    '''
    return hex(getptr(buff))

def create_buff_str(string:str, encoding:str='utf8'):
    string += '\0\0'
    bytes_ = string.encode(encoding)
    buff = create_string_buffer(bytes_)
    return (buff, sizeof(buff), getptrhex(buff))

class Lep_Ahkh2_Orgin:

    ah2dll:ctypes.CDLL = None

    @staticmethod
    def settypes(ah2dll:ctypes.CDLL):
        '''该dll导出函数皆为CDecl Call'''    
        # ah2dll.MinHookEnable.restype=
        # ah2dll.MinHookEnable.argtypes=

        # ah2dll.MinHookDisable.restype=
        # ah2dll.MinHookDisable.argtypes=

        # ah2dll.g_ThreadExitApp.restype=
        # ah2dll.g_ThreadExitApp.argtypes=

        # ah2dll.g_FirstThreadID.argtypes=
        # ah2dll.g_FirstThreadID.restype=

        # (Script, cmd, Title) 
        # -> ThreadID: 线程id
        ah2dll.NewThread.restype=c_uint
        ah2dll.NewThread.argtypes=[c_wchar_p, c_wchar_p, c_wchar_p]

        # (ThreadID) 
        # -> IsRunning: 1 正在运行 0 不在运行
        ah2dll.ahkReady.restype=c_int
        ah2dll.ahkReady.argtypes=[c_uint]

        # (FuncName, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, ThreadId) 
        # -> IsCalled: 1 找到函数并已调用, 0 未找到函数并未调用
        ah2dll.ahkPostFunction.restype=c_uint
        ah2dll.ahkPostFunction.argtypes=[c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_uint]
        
        # (PauseFlag, ThreadId) : PauseFlag: 字符串 On / Off / TRUE / FALSE / 1 / 0 
        # -> IsPaused: 1 已暂停 0 
        ah2dll.ahkPause.restype=c_int
        ah2dll.ahkPause.argtypes=[c_wchar_p, c_uint]

        # (LabelName, IsWait, ThreadId) : IsWait: 整数 1 等待label执行结束, 0 不等待
        # -> IsLabelFoundAndExec: 标签找到并执行了 
        ah2dll.ahkLabel.restype= c_int
        ah2dll.ahkLabel.argtypes= [c_wchar_p, c_uint, c_uint]

        # (VarName, GetVarPointer, ThreadId): GetVarPointer: 1 获取指针 0 获取内容
        # -> VarPointer: 指针或内容
        ah2dll.ahkgetvar.restype=c_void_p
        ah2dll.ahkgetvar.argtypes= [c_wchar_p, c_uint, c_uint]

        # (FuncName, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, ThreadID)
        # -> ReturnStr: ahk函数返回值
        ah2dll.ahkFunction.restype=c_wchar_p
        ah2dll.ahkFunction.argtypes=[c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_uint]

        # (LabelName, ThreadId)
        # -> LabelPointer: 标签指针, 返回0没找到标签
        ah2dll.ahkFindLabel.restype=c_void_p
        ah2dll.ahkFindLabel.argtypes=[c_wchar_p, c_uint]
        
        # (FuncName, ThreadId)
        # -> FuncPointer: 函数指针, 返回0没找到函数
        ah2dll.ahkFindFunc.restype=c_void_p
        ah2dll.ahkFindFunc.argtypes=[c_wchar_p, c_uint]

        # (LinePointer, Mode, ThreadId): Mode: 0 执行且返回下一行的指针 / 1 UNTIL_RETURN 直到遇到return / 2 UNTIL_BLOCK_END / 直到block块结束 / 3 ONLY_ONE_LINE 仅执行这一行
        # -> NextLinePointer: 下一行的函数指针
        ah2dll.ahkExecuteLine.restype=c_void_p
        ah2dll.ahkExecuteLine.argtypes=[c_void_p, c_uint, c_uint]

        # (Script, ThreadId)
        # -> IsExecSuccess: 1 执行成功 0 执行失败
        ah2dll.ahkExec.restype=c_uint
        ah2dll.ahkExec.argtypes=[c_wchar_p, c_uint]

        # (VarName, Value, ThreadId)
        # -> IsAssignSuccess: -1 失败 0 成功
        ah2dll.ahkassign.restype=c_int
        ah2dll.ahkassign.argtypes=[c_wchar_p, c_wchar_p, c_uint]

        # (NewCode, WaitExecute, ThreadId): WaitExecute: 0 仅添加代码, 不执行 / 1 添加代码且等待执行代码直到遇上return / 2 添加代码且立刻返回(不等待它执行完毕)
        # -> LinePointerOfNewCode
        ah2dll.addScript.restype=c_void_p
        ah2dll.addScript.argtypes=[c_wchar_p, c_int, c_uint]

    def __init__(self, dllpath) -> None:
        self.dllpath = dllpath
        self.ah2dll:ctypes.CDLL = Lep_Ahkh2_Orgin.ah2dll if Lep_Ahkh2_Orgin.ah2dll else ctypes.cdll.LoadLibrary(dllpath)

        # self.ah2dll:ctypes.CDLL = ctypes.cdll.LoadLibrary(dllpath)


        Lep_Ahkh2_Orgin.settypes(self.ah2dll)

class Lep_Ahkh2(Lep_Ahkh2_Orgin):
    ''' AHK阻塞执行 '''
    def __init__(self, dllpath:str='', title:str='', cmdline:str='') -> None:
        '''dllpath第一次初始化要填路径, 最好是完整路径, 成功载入之后该参数无效'''
        super().__init__(dllpath)

        self._return_size_buff_type_str = 'UInt'
        self._return_size_buff_type = c_uint
        self._return_size_buff = self._return_size_buff_type(0)
        self._return_size_ptr_hex = getptrhex(self._return_size_buff)

        self._return_buffptr_type_str = 'Ptr'
        self._return_buffptr_type = c_void_p
        self._return_buffptr_buff = self._return_buffptr_type()
        self._return_buffptr_ptr_hex = getptrhex(self._return_buffptr_buff)

        self.title = ''
        self.threadid = self.ah2dll.NewThread('#NoTrayIcon\nPersistent True', cmdline, title)
        while not self.ah2dll.ahkReady(self.threadid):
            pass

        self.pyfncbmap = {}
        def pyfncb(cbinfo)->c_wchar_p:
            cbinfo = json.loads(cbinfo)
            # print(cbinfo)
            fn = self.pyfncbmap[cbinfo['fnnamepy']]
            res = fn(*cbinfo['args'])
            if (res is None) or (res == ''): 
                self.do("""_pyreturn_temp := '[""]'""")
            else:
                sret:str = json.dumps([res]) + '\0\0'
                bret:bytes = sret.encode('utf-8')
                
                buff = create_string_buffer(len(bret))
                buff.value = bret
                buff_ptrhex:str = getptrhex(buff)
                self.do(f"_pyreturn_temp := StrGet({buff_ptrhex}, 'utf-8')")
                buff = ''

        self.pyfncb = ctypes.CFUNCTYPE(c_void_p, c_wchar_p)(pyfncb)
        self.pyfncb_hexptr = hex(cast(self.pyfncb, c_void_p).value)
        self.add(f'''
            global _return := ''
            global _return_buff := ''

            global _pyreturn_temp := ''

            __pyhkcb(pyfnname) {{
                %pyfnname%(A_ThisHotkey)
            }}
            __pyfncb(cbinfo) {{
                global _pyreturn_temp
                local res
                DllCall({self.pyfncb_hexptr}, 'WStr', cbinfo, 'CDecl')
                res := JSON.parse(_pyreturn_temp)[1]
                return res
            }}
            __return_emtpy() {{
                global _return
                _return:= ""
            }}
            __return_ensure() {{
                global _return, _return_buff
                ; 类型为字符串时

                _return_buff := ""
                if (strlen(_return) < 1) {{
                    NumPut('{self._return_size_buff_type_str}', 0, {self._return_size_ptr_hex})
                }} else {{
                    size := StrPut(_return, 'utf-8') + 2
                    NumPut('{self._return_size_buff_type_str}', size, {self._return_size_ptr_hex})
                    _return_buff := Buffer(size, 0)
                    NumPut('{self._return_buffptr_type_str}', _return_buff.ptr, {self._return_buffptr_ptr_hex})
                    StrPut(_return, _return_buff, 'utf-8')
                }}
            }}

            return
        ''' )
    
    def add_pyfn(self, pyfunc, alias:str=''):
        '''
            pyfunc: python函数
            alias: ahk调用所用的函数名, 默认为空, 即用的python的函数名
        '''
        fnnamepy = pyfunc.__name__
        fnnameahk = alias if alias else pyfunc.__name__
        self.pyfncbmap[fnnamepy] = pyfunc
        self.add(f"""
            {fnnameahk}(args*) {{
                return __pyfncb(JSON.stringify({{fnnamepy: '{fnnamepy}', args: args}}))
            }}
            return
        """)
        return (fnnamepy,fnnameahk)

    def add_pyhk(self, hotkey:str, pyfunc, alias:str=''):
        (fnnamepy,fnnameahk) = self.add_pyfn(pyfunc, alias)
        self.add(f'{hotkey}::__pyhkcb("{fnnamepy}")\n')

        
    def setval(self, name:str, value):
        '''设置线程中的全局变量'''
        if value == '':
            self.add(f'global {name} := ""')
        else:
            (buff, size, ptrhex) = create_buff_str(json.dumps([value]))
            self.add(f'global {name} := StrGet({ptrhex}, "utf-8")\n{name} := JSON.parse({name})[1]')
            del buff

    
    def getval(self, name:str):
        '''读取线程中的全局变量'''
        return self.do(f'global _return, {name}\n_return := {name}')


    def __del__(self):
        # print('结束线程')
        if self.ah2dll.ahkReady(self.threadid):
            self.do('ExitApp(0)')

    def isrunning(self):
        return self.ah2dll.ahkReady(self.threadid)

    def add(self, ahkscript:str):
        '''
            添加ahk代码, 永久保留此代码
            请勿去掉sleep 函数, 否则可能报错
        '''

        self.ah2dll.addScript(ahkscript, 1, self.threadid)
    
    def add_file(self, ahkfile:str, encoding='utf-8'):
        '''
            从文件添加ahk代码, 永久保留此代码
        '''
        with open(ahkfile, 'r', encoding=encoding) as f:
            script = f.read()
            f.close()
        self.add(script)


    def do(self, ahkscript:str)->str:
        '''
            立即执行ahk代码, 为 ahk变量 _return 赋值将输出为字符串, 将作为 do() 的返回值, 类型为python的str
        '''
        self.ah2dll.ahkExec(f"__return_emtpy()\n{ahkscript}\n__return_ensure()", self.threadid)
        size = self._return_size_buff.value
        if size > 0:
            ptr = self._return_buffptr_buff.value
            if ptr > 0:
                return getptrstr(ptr, size, 'utf-8').rstrip('\0')
        else:
            return ''

    def doj(self, ahkscript:str)->str:
        '''
            立即执行ahk代码, 将 ahk 变量_return赋值为 map, array 或者 object 类型数据, 将作为 doj() 的返回值, 类型为 python 的 dict 或者 list
        '''
        end = '''
        try {
            if (_return) {
                _return := JSON.stringify(_return)
            } else {
                _return := ""
            }
        } catch {
            _return := ""
        }
        '''
        res = self.do(f'{ahkscript}\n{end}')
        
        if (res):
            res = json.loads(res)
            return res
        else:
            return None
    """
        def fn_backup(self, fnname:str, *args):
            '''
                该函数不稳定, 第 4095 次调用闪退程序
                for i in range(0, 9999999)
                print(ah2.fn('你好', f'你好{i}这么多次'))
            '''
            raise Exception('该函数不可用')
            arglen = len(args)
            if arglen > 10: raise Exception('不允许传入10个以上的参数')
            argsls = []
            argsls.extend(args)
            argsls.extend(['' for _ in range(0, 10 - arglen)])
            argsls.append(self.threadid)
            return self.ah2dll.ahkFunction(fnname, *argsls)
    """


def pyhotkey(A_ThisHotkey):
    for i in range(0, 99):
        print(f'你按下了热键[{A_ThisHotkey}]{i}次')

def pyfn(ls):
    return {'hello': f'world...{ls[0]}' }

if __name__ == '__main__':
    ah2dll32 = f'{get_main_dir()}\\bin\\ahkh2x32mt.dll'
    ah2dll64 = f'{get_main_dir()}\\bin\\ahkh2x64mt.dll'
    dllpath = ah2dll32 if is32ptr() else ah2dll64


    ah2 = Lep_Ahkh2(dllpath)
    ah2.setval('abc', '123')
    ah2.setval('abc', '567')
    print(ah2.getval('abc'))

    while (True):
        sleep(1)
        