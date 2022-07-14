import webview

'''
    注意事项:
        0. pip install pywebview
        1. 只能在python主线程运行, 或者用multiprocessing 库执行
        2. 运行此功能需要安装webview2 runtime: https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section
        3. pywebview 官网: https://pywebview.flowrl.com/

    调用示例:
    import webview
    class PyApi4Js:
        def __init__(self):
            self.window:webview.Window = None

        # window.pywebview.api.print({a:123})
        def print(self, dic:dict):
            print(dic)

    Lep_Webview2(pyapi4js=PyApi4Js())

'''

def Lep_Webview2(
    start_url:str='about:blank', 
    pyapi4js:object=None, 
    js_onload:str='', 
    title:str='Webview2 GUI', 
    min_size:tuple=(500, 500), 
    debug:bool=True
):
    '''
        url:        窗体载入时打开的url
        pyapi4js:   任意class创建对象, 用于给js提供接口, 注意
            1. 将 映射为 js 中的 window.pywebview.api
            2. 执行js有延迟, 需要等待 window.hasOwnProperty('pywebview') && window.pywebview.hasOwnProperty('api')
            3. 所有类中的方法被映射为js 的 async 异步函数
        js_onload:  在页面刷新时候执行的js代码
        title: 标题
    '''

    def wvOnLoad(window:webview.Window):
        result = window.evaluate_js(js_onload)

    def wvOnClosed():
        print('窗口被关闭')
        pass
    para = {}
    if pyapi4js: para['js_api'] = pyapi4js
        
    window = webview.create_window(title=title, url=start_url, min_size=min_size, **para)
    if pyapi4js: 
        try:
            getattr(pyapi4js, 'window')
            pyapi4js.window = window
        except Exception as e:
            print('请在js_api中预留一个self.window属性, 以注入此window对象')

    window.events.closed += wvOnClosed
    webview.start(wvOnLoad, window, debug=debug)