import requests

def getDictSocks5Auth(user, pswd, ip, port):
    ''' 必须安装pysocks, "pip install pysocks" 格式如: {'http': 'socks5://user:pswd@127.0.0.1:1080', 'https': 'socks5://user:pswd@127.0.0.1:1080'} 
    '''
    socks5 = f'socks5://{user}:{pswd}@{ip}:{port}'
    return {'http': socks5, 'https': socks5}


def getDictSocks5(ip, port):
    ''' 必须安装pysocks "pip install pysocks", 格式如: {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'} '''
    socks5 = f'socks5://{ip}:{port}'
    return {'http': socks5, 'https': socks5}


def getHttpProxies(ip, port):
    ''' http://ip:port '''
    pre = f'://{ip}:{port}'
    return {'http': f'http{pre}', 'https': f'https{pre}'}

def checkMyIp(ip:str, proxies=None, useprint=True):
    ''' 通过请求 'https://api.myip.com' 获取当前 ip, result, errmsg = checkMyIp('10.10.10.10') '''
    para = {}
    para['verify'] = False
    para['timeout'] = 3
    if proxies:
        para['proxies'] = proxies
    try:
        res = requests.get('https://api.myip.com', **para)
        if res.status_code == 200 :
            resj:dict = res.json()
            if resj.__contains__('ip'): 
                if useprint: print(f'本机网络ip为:{resj["ip"]}')
                if (resj['ip'] == str(ip)):
                    return (True, '')
            else:
                if useprint: print('未获取到ip, 返回内容:', resj)
        else:
            if useprint: print('未获取到ip, 返回内容:', res.content)
        return (False, res.content)
    except Exception as e:
        return (False, f'checkMyIp()发生异常,异常类型{type(e).__name__}')

if __name__ == '__main__':
    checkMyIp('10.10.10.10')