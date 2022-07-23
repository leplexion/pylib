from ctypes import create_string_buffer, string_at,sizeof, cast, POINTER, pointer, c_char, c_void_p, _SimpleCData, c_int
import ctypes
import re

# 第三方库
import chardet


def hexstr2bytes(hexstr:str):
    '''hexstr: 16进制字符串, 如 "AA BB FF 01 05, 将删除所有空格, 1个字节占2位符号, 即必须偶数个字符串" '''
    hexstr = re.sub(r'\s+', '', hexstr)
    chrlen = len(hexstr)
    if chrlen > 0 and divmod(chrlen, 2)[1] == 0:
        blist = [ int(hexstr[i:i+2], 16) for i in range(0, chrlen, 2) ]
        return bytes(blist)
    else:
        raise Exception('hexstr长度必须为偶数位')


def test_encoding_hexstr(hexstr:str):
    '''检测字符串编码: 从二进制 hex 文本'''
    buff = Lep_Buffer.create_from_hex_str(hexstr)
    return chardet.detect(buff.raw)

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


class Lep_Buffer:

    __buff = None   # python 的对象

    def __del__(self):
        pass

    def __getitem__(self, subscript):
        '''切片: 下标单位返回 int, 切片返回 list[int]'''
        res = self.raw.__getitem__(subscript)
        if isinstance(subscript, slice):
            return list(bytes(res))
        else:
            return int(res)

    def __len__(self):
        return self.size
    
    def __iter__(self): 
        idx = -1
        for byte in self.raw:
            idx += 1
            yield (byte, idx)

    @staticmethod
    def create(size:int):
        if type(size) is not int: raise Exception(f'size不允许为int类型以外的参数, 你输入了{size},类型:{type(size).__name__}:')
        if size < 1: raise Exception(f'size不允许是小于1的int整数')
        buff = Lep_Buffer()
        buff.__buff = (c_char * size)()
        return buff

    @staticmethod
    def create_from_bytes(raw:bytes):
        if type(raw) is not bytes: raise Exception(f'raw不允许为bytes类型以外的参数, 你输入了{raw},类型:{type(raw).__name__}:')
        buff = Lep_Buffer()
        buff.__buff = (c_char * len(raw))()
        buff.__buff.value = raw
        return buff
    
    @staticmethod
    def create_from_file(file:str):
        with open(file, 'rb') as f:
            b = f.read()
            f.close()
        buff = Lep_Buffer.create_from_bytes(b)
        return buff

    @staticmethod
    def create_from_str(s:str, encoding:str='utf-8', end='\0\0'):
        if len(s) < 1: raise Exception(f'string参数字符串长度不允许小于1')
        return Lep_Buffer.create_from_bytes(f'{s}{end}'.encode(encoding))

    @staticmethod
    def create_from_ptr(ptr, size:int):
        if size < 1: raise Exception(f'创建buffer尺寸不允许小于{size}')
        buff = Lep_Buffer()
        buff.__buff = (c_char * size).from_address(ptr)
        return buff

    @staticmethod
    def create_from_hex_str(hexstr:str):
        '''hexstr: 16进制字符串, 如 "AA BB FF 01 05, 将删除所有空格, 1个字节占2位符号, 即必须偶数个字符串" '''
        hexstr = re.sub(r'\s+', '', hexstr)
        chrlen = len(hexstr)
        if chrlen > 0 and divmod(chrlen, 2)[1] == 0:
            blist = [ int(hexstr[i:i+2], 16) for i in range(0, chrlen, 2) ]
            return Lep_Buffer.create_from_bytes(bytes(blist))
        else:
            raise Exception('hexstr长度必须为偶数位')

    @staticmethod
    def create_from_file_hex_str(file):
        with open(file, 'r', encoding='utf-8') as f:
            hexstr = f.read()
            f.close()
        return Lep_Buffer.create_from_hex_str(hexstr)

    @staticmethod
    def create_from_Lep_Buffer(buff):
        return buff.copy()

    @property
    def size(self): 
        return sizeof(self.__buff)

    @property
    def ptr(self): 
        return cast(self.__buff, c_void_p).value

    @property
    def ptrhex(self):
        return hex(self.ptr)

    @property
    def raw(self)->bytes:
        return self.__buff.raw

    @property
    def raw_byte_list(self)->list:
        return [byte for byte in self.raw]

    @property
    def raw_hex_str(self)->str:
        return ''.join(['%02x' % byte for byte in self.raw])

    def save_file(self, file:str)->None:
        with open(file, 'wb') as f:
            f.write(self.raw)
            f.close()

    def get_hex_str(self, delm:str=' ', warp_count=16)->str:
        res = ''
        idx = 1
        for byte in self.raw:
            if warp_count > 0 and divmod(idx, warp_count)[1] ==0 and idx != 0: 
                res += '%02x' % byte + '\n'
            else:
                res += '%02x' % byte + delm
            idx += 1
        return res

    def get_hex_str_sub(self, start:int, length:int, delm:str=' ', warp_count=0):
        res = ''
        idx = 1
        for byte in self.raw[start: start + length]:
            if warp_count > 0 and divmod(idx, warp_count)[1] ==0 and idx != 0: 
                res += '%02x' % byte + '\n'
            else:
                res += '%02x' % byte + delm
            idx += 1
        return res

    def fill_bytes(self, byte:int)->None:
        self.__buff.value = bytes([ byte for _ in range(0, self.size) ])

    def resize(self, newsize:int, keepdata:bool=True, autoslice:bool=False):
        '''如果尺寸不一致, 将重置内存地址'''
        if newsize == self.size: 
            if not keepdata:
                self.fill_bytes(0)
            return
        if newsize < 1: raise Exception('新的内存地址不得小于1')
        if keepdata:
            bytes_ = self.raw
            if newsize < self.size:
                if not autoslice:
                    raise Exception('新尺寸小于旧尺寸, 无法放置旧数据, 请设置 autoslice 为 True 消除此异常')
                bytes_ = bytes_[:newsize]
            self.__buff = (c_char * newsize)()
            self.__buff.value = bytes_
        else:
            self.__buff = (c_char * newsize)()

    def get_bytes(self)->bytes:
        return self.raw

    def set_bytes(self, raw:bytes, offset:int=0, autoslice:bool=False):
        '''
            不改变原来地址, 设置二进制数据
            autoslice: 超出长度的部分是否被截取, False 在超出长度时抛出异常
        '''
        wsize = len(raw)
        ssize = self.size

        if wsize < 1: raise Exception('写入的bytes长度不允许小于1')
        if offset >= ssize: raise Exception('偏移超出该buffer尺寸')

        overflow = wsize + offset > ssize
        if (not autoslice) and overflow: 
            raise Exception('写入的字节将超出该buffer内存的长度')
        elif autoslice and overflow:
            slice_size = ssize-offset
            (c_char * slice_size).from_address(self.ptr+offset).value = raw[:slice_size]
        else:
            (c_char * wsize).from_address(self.ptr+offset).value = raw

    def get_str(self, encoding:str='utf-8')->str:
        return self.raw.decode(encoding=encoding)

    def copy(self):
        return Lep_Buffer.create_from_bytes(self.raw)

    def copy2ptr(self, ptr:int):
        (c_char * self.size).from_address(ptr).value = self.raw

    def reverse(self):
        bls = list(self.raw)
        bls.reverse()
        self.__buff.value = bytes(bls)
        return self

if __name__ == '__main__':
    # i = c_int(123)
    # print(getptrnum(p, c_int))
    # print(getbuffptr(i))
    b = Lep_Buffer.create_from_str('你好世界')
    print(getptrstr(b.ptr, b.size, 'utf-8'))