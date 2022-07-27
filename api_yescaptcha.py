import requests


ReCapv3Types = [
    'RecaptchaV3TaskProxyless',
    'RecaptchaV3Task'
    'RecaptchaV3TaskProxylessM1',
    # 'RecaptchaV3TaskM1',  # 不确定
    'RecaptchaV3EnterpriseTask',
]

class ReCapv3Proxy:
    '''
    proxyType
    proxyAddress
    proxyPort
    proxyLogin
    proxyPassword
    '''
    pass



class ReCapv3:

    # 缺省时
    _clientKey  = None
    api_site    = 'https://api.yescaptcha.com/createTask'
    '''
    国际节点: https://api.yescaptcha.com
    国内节点: https://china.yescaptcha.com
    请求格式：POST application/json
    '''

    def __init__(self, websiteURL:str, websiteKey:str, pageAction:str, clientKey:str=None, _type:str = 'RecaptchaV3TaskProxyless') -> None:
        '''
        websiteURL: 从请求 https://www.google.com/recaptcha/xxxx 请求头中的refer 
        websiteKey:  从目标网页上找到类似 grecaptcha.execute('6LewTP8UAAAAAI3855Ww2s7yBxkXrdvNOJo2ycKC', {action: 'write/item'}) 
        pageAction: 如上参数
        '''
        if _type not in ReCapv3Types: raise Exception('_type值应为ReCapv3Types中的值')

        self.type = _type
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.pageAction = pageAction

        if clientKey:
            self.clientKey  = clientKey 
        elif ReCapv3._clientKey:
            self.clientKey  = ReCapv3._clientKey
        else:
            raise Exception('必须设置clientKey')

        # 创建task的时候返回
        self.taskId = None
        self.result = None
        self.success = False

    def api_createTask(self):
        '''
        {
            "errorId": 0,
            "errorCode": "",
            "errorDescription": "",
            "taskId": "61138bb6-19fb-11ec-a9c8-0242ac110006" // 请记录此ID
        }
        '''
        url = f'{ReCapv3.api_site}/createTask'
        data = {
            "clientKey": self.clientKey,
            "task": {
                "websiteURL" : self.websiteURL,
                "websiteKey" : self.websiteKey,
                "pageAction" : self.pageAction,
                "type" : self.type
            }
        }
        return requests.post(url=url, json=data, verify=False)
    
    def api_getTaskResult(self):
        if not self.taskId:
            raise Exception('未获取taskId无法调用此接口')

        url = f'{ReCapv3.api_site}/getTaskResult'
        data = {
            "clientKey": self.clientKey,
            "taskId": self.taskId
        }
        return requests.post(url=url, json=data, verify=False)
        

        