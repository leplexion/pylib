import requests
import requests.utils

def cookieStr2Dict(cookies:str):
    cookie_dic = {}
    for i in cookies.split('; '):
        cookie_dic[i.split('=')[0]] = i.split('=')[1]
    return cookie_dic

def cookieDict2Str(cookies:dict):
    return requests.utils.cookiejar_from_dict(cookies)

def parseCookie(cookie:str)->dict:
    ''' 解析从谷歌浏览器复制黏贴的cookie '''
    if cookie == '': raise Exception('cookie 不允许未空')
    sstart = 'cookie: '
    cookie=cookie.strip(' ')
    if cookie.startswith(sstart):
        cookie = cookie[len(sstart):]
    res:dict = {}
    cookiepairs = cookie.split(' ')
    cookiepair:str = ''
    for cookiepair in cookiepairs:
        cookiepair=cookiepair.strip(' ')
        if cookiepair.startswith('=') or cookiepair.endswith('='):
            raise Exception(f'解析cookie错误: 遭遇开头或尾部={cookiepair}')
        cookiepairls= cookiepair.split('=')
        if len(cookiepairls) != 2:
            raise Exception(f'解析cookie错误: 获得超过不等于2位的键值对 {cookiepair}')
        val:str = cookiepairls[1]
        res[cookiepairls[0]] = val if not val.endswith(';') else val[:-1]
    # a = res.keys
    if len(res) < 1:
        raise Exception(f'解析cookie错误: 未成功解析cookie内容')
    return res
