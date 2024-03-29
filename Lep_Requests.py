import requests
import requests.utils
from requests import Response, Session
import urllib3
import urllib.parse

try:
    from .lep_print import print_e
    from .Lep_Requests_Url import *
    from .Lep_Requests_Proxies import *
    from .Lep_Requests_Cookie import *
    from .Lep_Requests_Headers import *
    from .lep_file import file_exist
except:
    from lep_print import print_e
    from Lep_Requests_Url import *
    from Lep_Requests_Proxies import *
    from Lep_Requests_Cookie import *
    from Lep_Requests_Headers import *
    from lep_file import file_exist

import mimetypes


def get_file_mimetype(path:str):
    '''获取(猜测)headers 中的 content-type 和 data: {mime-type}'''
    if not file_exist(path):
        raise Exception(f'get_file_mimetype函数错误,路径不存在: {path}')
    res: tuple = mimetypes.guess_type(path, strict=True)
    if res is None:
        raise Exception(f'get_file_mimetype函数错误,返回错误')
    return res[0]

def get_image_data_base64(path:str):
    '''获取图像"data:{meme_type};base64,"形式的编码'''
    mimetype = get_file_mimetype(path)
    if not mimetype.startswith('image/'):
        raise Exception(f'get_image_data_base64函数错误,文件mimetype非图像类型{path}')
    res:str = f'data:{mimetype};base64,'
    return res

def get_image_data_base64_url(path:str):
    '''同get_image_data_base64, 经过uri转码'''
    return encodeUriComponent(get_image_data_base64(path))

def diable_urilib3_warnings():  # 禁用 ssl 警告
    urllib3.disable_warnings()

class LepRequests:

    @staticmethod
    def getSocks5HttpProxies1(user, pswd, ip, port): # 用于requests proxies请求, 需要安装 pip install pysocks
        socks5 = f'socks5://{user}:{pswd}@{ip}:{port}'
        return {'http': socks5, 'https': socks5}

    @staticmethod
    def getSocks5HttpProxies2(ip, port): # 用于requests proxies请求, 需要安装 pip install pysocks
        socks5 = f'socks5://{ip}:{port}'
        return {'http': socks5, 'https': socks5}
    
    def __init__(self, 
            cookie:dict=None,  
            timeout:int=None, 
            proxies:dict=None, 
            headers:dict =None, 
            verify:bool=None
        ) -> None:
        self.reqidx:int = None
        self.para:dict = {}
        if timeout  is not None: self.para['timeout']   = timeout
        if proxies  is not None: self.para['proxies']   = proxies
        if headers  is not None: self.para['headers']   = headers
        if verify   is not None: self.para['verify']    = verify
        
        self.session:Session = requests.session()
        if cookie: requests.utils.add_dict_to_cookiejar(self.session.cookies, cookie)

    def getcookie(self)->dict:
        return self.session.cookies.get_dict()
        
    def get(self, url, isJoinHeaders:bool = False,**para)->Response:
        reqpara = {}
        for k in self.para: reqpara[k]   = self.para[k]
        for k in para: reqpara[k]        = para[k]

        if isJoinHeaders:
            isParaHeader = para.__contains__('headers')
            isSelfParaHeader = self.para.__contains__('headers')
            if isParaHeader and isSelfParaHeader:
                reqheaders = {}
                if isSelfParaHeader:
                    for k in self.para['headers']: reqheaders[k]   = self.para['headers'][k]
                if isParaHeader:
                    for k in para['headers']: reqheaders[k] = para['headers'][k]
                reqpara['headers'] = reqheaders
        try: 
            self.lastres = self.session.get(url, **reqpara)
            return self.lastres
        except Exception as e: 
            # print('请求错误')
            raise e
    def post(self, url, isJoinHeaders:bool = False,**para)->Response:
        reqpara = {}
        for k in self.para: reqpara[k]   = self.para[k]
        for k in para: reqpara[k]        = para[k]
        if isJoinHeaders:
            isParaHeader = para.__contains__('headers')
            isSelfParaHeader = self.para.__contains__('headers')
            if isParaHeader and isSelfParaHeader:
                reqheaders = {}
                if isSelfParaHeader:
                    for k in self.para['headers']: reqheaders[k]   = self.para['headers'][k]
                if isParaHeader:
                    for k in para['headers']: reqheaders[k] = para['headers'][k]
                reqpara['headers'] = reqheaders
        try: 
            self.lastres = self.session.post(url, **reqpara)
            return self.lastres
        except Exception as e: 
            # print('请求错误')
            raise e

if __name__ == '__main__':
    # print(cookieStr2Dict('yandexuid=1895670281657529799; yuidss=1895670281657529799; i=h+wh9pItRSyhKlw4GthKt6liw6FoEPiEO2loGZDOvHzM/ZN8a0fV57Qljtb4XZFHN4oi+ueQ+1hXXC2Ow/4RF9Vgp0M=; yandex_gid=87; is_gdpr=0; is_gdpr_b=CI+ICxDwfQ==; yp=1657939556.yu.1895670281657529799; ymex=1660445156.oyu.1895670281657529799#1689138965.yrts.1657602965#1689139825.yrtsi.1657603825; sync_cookie_ok=synced; yabs-sid=850611151657933394'))
    a = get_file_mimetype('C:\\Users\\DY-I7\\Desktop\\bcd.jpg')
    pass