import requests
import json
import re
import requests.utils

try:
    from .Lep_Requests import encodeUriComponent, diable_urilib3_warnings, urlpath2FileName, urlClearQuery
    from .Lep_Requests_Proxies import getDictSocks5, getHttpProxies
    from .Lep_Requests_Headers import HeaderLoader
    from .Lep_Requests_Url import urlClearQuery
    from .lep_json import jsonpretty
    from .lep_time import get_now_acc_msec
    from .lep_rand import randintzfill
    from .lep_folder import folder_create
    from .lep_ctypes import hexstr2bytes
    from .lep_file import filewriteb

except Exception as e:
    from Lep_Requests import encodeUriComponent, diable_urilib3_warnings, urlpath2FileName, urlClearQuery
    from Lep_Requests_Proxies import getDictSocks5, getHttpProxies
    from Lep_Requests_Headers import HeaderLoader
    from Lep_Requests_Url import urlClearQuery
    from lep_json import jsonpretty
    from lep_time import get_now_acc_msec
    from lep_rand import randintzfill
    from lep_folder import folder_create
    from lep_ctypes import hexstr2bytes
    from lep_file import filewriteb


class Lep_ReqBase:

    def __init__(self, proxies:dict=None, cookies:dict=None, dump_enable:bool=False, timeout:int=5) -> None:
        self.req                = requests.session()
        self.good_uploads:list  = []
        self.proxies:dict       = proxies
        self.timeout:int        = timeout

        self.cookies_set(cookies=cookies)
        
        if dump_enable:
            self.dump_enable = dump_enable
            self.dumpdir = f'./dump/{get_now_acc_msec()}{randintzfill(5)}'
            self.dumpidx = 0
            self.dump_method  = ''
            self.dump_this_dir = ''
            self.dump_this_url = ''
            self.dumpinit = False
            print(f'请求dump创建文件夹:{self.dumpdir}')
            folder_create(self.dumpdir)
            setattr(self.req, 'dump_hook', [self.request_dump_hook])

    @property
    def request_dump_hook(self):

        '''
            prep = self.prepare_request(req)

            # D:\\py\\py38-32\\Lib\\site-packages\\requests\\sessions.py
            # request 库 session.py 文件 575 行左右, 添加以下3行代码
            if (hasattr(self, 'dump_hook')):
                print('requests 注入 session dump_hook')
                getattr(self, 'dump_hook')[0](prep)
        '''

        def dump_hook(prep_request_args):
            self.dumpidx += 1
            path_url = urlClearQuery(prep_request_args.path_url)
            
            dump_this_dir = f'{self.dumpdir}\\{self.dumpidx}-{self.dump_method}{urlpath2FileName(path_url)}'
            folder_create(dump_this_dir)
            dump_this_file = f'{dump_this_dir}\\requests.txt'
            
            url:str         = prep_request_args.url
            url_path:str    = prep_request_args.path_url
            headers:str     = jsonpretty(dict(prep_request_args.headers))
            cookies:str     = jsonpretty(requests.utils.dict_from_cookiejar(prep_request_args._cookies))
            body_txt:str    = str(prep_request_args.body)
            body_raw:bytes  = prep_request_args.body

            self.dump_this_url = url
            self.dump_this_dir = dump_this_dir

            with open(dump_this_file, 'w', encoding='utf-8') as f:
                f.write(f"""
{'=' * 60}
--- url ---
{url}

--- url_path ---
{url_path}

--- headers --- 
{headers}

--- cookies ---
{cookies}

--- body text ---
{body_txt}
{'=' * 60}
                """)
                f.close()
            if body_raw is None:
                with open(f'{dump_this_file}.body.bin', 'wb') as f:        
                    f.write(b'')
                    f.close()
            elif type(body_raw) is bytes:
                with open(f'{dump_this_file}.body.bin', 'wb') as f:        
                    f.write(body_raw)
                    f.close()
            elif type(body_raw) is str:
                with open(f'{dump_this_file}.body.bin', 'w', encoding='utf-8') as f:
                    f.write(body_raw)
                    f.close()
        return dump_hook

    def response_dump(self, res:requests.Response):
        res_code        = res.status_code
        res_headers     = jsonpretty(dict(res.headers))
        res_data_bytes  = res.content

        try:
            res_data_json = jsonpretty(json.loads(res.text))
        except Exception as e:
            res_data_json   = ''   

        try:
            res_data_text = res.text
        except Exception as e:
            res_data_text   = ''
        
        dump_this_dir = self.dump_this_dir
        dump_this_file = f'{dump_this_dir}\\response.txt'
        with open(dump_this_file, 'w', encoding='utf-8') as f:
            f.write(f"""
{'=' * 60}
--- code ---
{res_code}

--- url ---
{self.dump_this_url}

--- headers --- 
{res_headers}

--- data text --- 
{res_data_text}

--- data json --- 
{res_data_json}

{'=' * 60}
                """)
            f.close()
        filewriteb(res_data_bytes, f'{dump_this_file}.content.txt')

    def get(self, url:str, params:dict = None, data=None, timeout:int=None, **extparas)->requests.Response:
        self.dump_method = 'GET'
        paras = {
            'url': url,
            'verify': False,
            'timeout': self.timeout
        }
        if self.proxies:    paras['proxies']    = self.proxies
        if params:          paras['params']     = params
        if data:            paras['data']       = data
        if timeout:         paras['timeout']    = timeout

        # sessions D:\py\py38-32\Lib\site-packages\requests\sessions.py 约575行 prepare_request 返回值为最终请求参数

        res = self.req.get(**paras, **extparas)
        if self.dump_enable: self.response_dump(res)


        res_code        = res.status_code
        res_headers     = jsonpretty(dict(res.headers))
        res_data_bytes  = res.content

        try:
            res_data_json = res.json()
        except Exception as e:
            res_data_json   = ''   

        try:
            res_data_text = res.text
        except Exception as e:
            res_data_text   = ''
        
        # dtxt, djson, draw, code, res_headers = self.get()
        return res_data_text, res_data_json, res_data_bytes, res_code, res_headers

    def post(self, url:str, params:dict = None, data=None, timeout:int=None, **extparas)->requests.Response:
        self.dump_method = 'POST'
        
        paras = {
            'url': url,
            'verify': False,
            'timeout': self.timeout
        }
        if self.proxies:    paras['proxies']    = self.proxies
        if params:          paras['params']     = params
        if data:            paras['data']       = data
        if timeout:         paras['timeout']    = timeout

        res:requests.Response = self.req.post(**paras, **extparas)

        if self.dump_enable: self.response_dump(res)

        res_code        = res.status_code
        res_headers     = dict(res.headers)
        res_data_bytes  = res.content

        try:
            res_data_json = res.json()
        except Exception as e:
            res_data_json   = ''   

        try:
            res_data_text = res.text
        except Exception as e:
            res_data_text   = ''
        
        # self.check_request_dump_hook()

        # dtxt, djson, draw, code, res_headers = self.post()
        return res_data_text, res_data_json, res_data_bytes, res_code, res_headers

    # def post_x_www_form_urlencoded(self, url:str, fields:dict, params:dict = None, data=None, timeout:int=None, **extparas)->requests.Response:
    #     return self.post(

    def cookies_get(self):
        return dict(self.req.cookies.get_dict())
        
    def cookies_set(self, cookies:dict = None):
        requests.utils.add_dict_to_cookiejar(self.req.cookies, cookies)
