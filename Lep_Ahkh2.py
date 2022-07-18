from cmath import e
import ctypes
from ctypes import c_int, c_uint, c_void_p, c_wchar_p, _SimpleCData, pointer, cast, string_at


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


class Lep_Ahkh2_Orgin:
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
        self.ah2dll:ctypes.CDLL = ctypes.cdll.LoadLibrary(dllpath)
        Lep_Ahkh2_Orgin.settypes(self.ah2dll)


class Lep_Ahkh2_OT(Lep_Ahkh2_Orgin):
    '''单线程执行工具'''
    def __init__(self, dllpath, title:str='') -> None:
        super().__init__(dllpath)

        self._return_size_buff_type_str = 'UInt'
        self._return_size_buff_type = c_uint
        self._return_size_buff = self._return_size_buff_type(0)
        self._return_size_ptr_hex = getptrhex(self._return_size_buff)

        self.title = ''
        self.threadid = self.ah2dll.NewThread('Persistent True', '', title)
        while not self.ah2dll.ahkReady(self.threadid):
            pass
        self.add_script('global _return := ""')
        self.add_script(f'''
            global _return := ""
            global _return_buff := ""
            __return_emtpy() {{
                global _return
                _return:= ""
            }}
            __return_ensure() {{
                global _return, _return_buff
                ; 类型为字符串时

                if (strlen(_return) < 1) {{
                    NumPut('{self._return_size_buff_type_str}', 0, {self._return_size_ptr_hex})
                }} else {{
                    size := StrPut(_return, 'utf-8') + 2
                    NumPut('{self._return_size_buff_type_str}', size, {self._return_size_ptr_hex})
                    _return_buff := Buffer(size)
                    StrPut(_return, _return_buff, 'utf-8')
                }}

                ; 类型为Map

                ; 类型为Array

                ; 类型为Object
            }}
        ''' )

    def add_script(self, ahkscript:str):
        '''添加ahk代码, 永久保留此代码'''
        self.ah2dll.addScript(ahkscript, 1, self.threadid)
    
    def add_script_file(self, ahkfile:str, encoding='utf-8'):
        '''从文件添加ahk代码, 永久保留此代码'''
        with open(ahkfile, 'r', encoding=encoding) as f:
            script = f.read()
            f.close()
        self.add_script(script)

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

    def do(self, ahkscript:str):


        self.ah2dll.ahkExec(f"__return_emtpy()\n{ahkscript}\n__return_ensure()", self.threadid)

    

if __name__ == '__main__':
    import platform
    dllpath = f"bin\\{ 'ahkh2x32mt.dll' if (platform.architecture()[0] == '32bit') else 'ahkh2x64mt.dll' }"
    ah2 = Lep_Ahkh2_OT(dllpath)

    # ah2.add_script('Msgbox "你好世界"')
    # ah2.do("Msgbox '再次你好世界'")

    ah2.add_script("""
    你好(p1) {
        
        return p1
    }
    """)

    for i in range(0, 9999999):
        print(ah2.fn('你好', f'你好{i}这么多次'))





    # threadid = ah2.ah2dll.NewThread('Persistent True', '', '')

    
    