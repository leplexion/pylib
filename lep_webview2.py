import webview
from .lep_file import fileread
from .lep_path import get_dir_list
from .lep_str import cut_text
import json
'''
    注意事项:
        0. pip install pywebview
        1. 只能在python主线程运行, 或者用multiprocessing 库执行
        2. 运行此功能需要安装webview2 runtime: https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section
        3. pywebview 官网: https://pywebview.flowrl.com/
        4. 其他资料: https://www.daimajiaoliu.com/daima/485b6d8319003fe

    调用示例:

# ------------------------------------------------------
from libpy.lep_file import fileread
from time import sleep
from libpy.lep_webview2 import Lep_Webview2, joinjs, PyApi4JsBase, joinjs2
import os
from libpy.lep_file import fileread
from time import sleep


class Api(PyApi4JsBase):
    def __init__(self) -> None: 
        super().__init__()

    @staticmethod
    def js_onload_func(): 
        jslibdir = 'libjs'
        jsmain = 'inject.fake.js'
        return  '(async function(window){\n' + joinjs2(jslibdir) + '\n' + fileread(jsmain) + '\n})(window);;'

if __name__ == '__main__':
    Lep_Webview2(js_onload_func=Api.js_onload_func, min_size=(1200, 800), pyapi4js=Api())
# ------------------------------------------------------
'''
from queue import Queue
class PyApi4JsBase:

    def __init__(self) -> None:
        self.window:webview.Window = None
        self.queue4jshook:Queue = Queue()

    def signal_put(self, signal): 
        self.queue4jshook.put(signal)
        self.window.evaluate_js('false')

    def print(self, *items):
        for item in items:
            print('[---js---]', item)


def joinjs(jsnames=[], dir=''):
    res:str = ''
    for jsname in jsnames:
        if dir:
            res += fileread(f'{dir}\{jsname}.js') + ';'
        else:
            res += fileread(f'{jsname}.js') + ';'
    return res


def joinjs2(dir:str):
    res = ''
    for path in get_dir_list(dir=dir, mode='ffullpath', ext='js'):
        res += fileread(path) + '\n'
    return res

def combineJsInnerAsyncCall(*jses):
    res = '(async function(window){\n'
    for js in jses:
        res += js + ';\n'
    res += '})(window);;'
    return res

def Lep_Webview2(
    start_url:str='about:blank', 
    pyapi4js:object=None, 
    title:str='Webview2 GUI', 
    min_size:tuple=(500, 500), 
    debug:bool=True,
    js_onload:str='', 
    js_onload_func = None,
    js_hook = None,
    onclosed = None
):
    '''
        url:        窗体载入时打开的url
        pyapi4js:   任意class创建对象, 用于给js提供接口, 注意
            1. 将 映射为 js 中的 window.pywebview.api
            2. 执行js有延迟, 需要等待 window.hasOwnProperty('pywebview') && window.pywebview.hasOwnProperty('api')
            3. 所有类中的方法被映射为js 的 async 异步函数
            4. 在 site-packages\webview\platforms\winforms.py 约228行添加 setattr(window, 'browser', self.browser), 可以取到原始的 webview2 对象
            5. window.browser.webview
        js_onload:  在页面刷新时候执行的js代码
        title: 标题
    '''

    para = {}
    if pyapi4js: para['js_api'] = pyapi4js
        
    window = webview.create_window(title=title, url=start_url, min_size=min_size, **para)
    if pyapi4js: 
        try:
            getattr(pyapi4js, 'window')
            pyapi4js.window = window
        except Exception as e:
            print('请在js_api中预留一个self.window属性, 以注入此window对象')
    # def wvOnDomLoad(window:webview.Window, ):

    def wvOnDomLoad():
        print(f'[webview2][事件] 页面dom加载完毕, 当前页:{window.get_current_url()}')
        js = ''
        if js_onload:
            js = js_onload
            print('[webview2][事件] 执行js.')
            
        if js_onload_func:
            print('[webview2][事件] 执行来自匿名函数返回的js代码.')
            js = js_onload_func()
            
        jsls = cut_text(js, 1000)

        window.evaluate_js('window._js=[];;')
        for js in jsls:
            window.evaluate_js(f'window._js.push({json.dumps(js)});;')
        window.evaluate_js('eval(window._js.join(""));;')

    def wvOnLoad(window:webview.Window):
        print('[webview2][事件]窗体已加载')
    
    def wvOnClosed():
        print('[webview2][事件] 窗口被关闭')
        if onclosed:
            print('[webview2][事件] 执行关闭回调')
            onclosed()

    def wvOnShow():
        print('[webview2][事件] 窗口已显示')

        def js_hook_outer(browser, script, id, callback):
            if js_hook and hasattr(window, 'browser'):
                CoreWebview2 = browser.web_view.CoreWebView2
                js_hook(pyapi4js, CoreWebview2, browser, script, id, callback)

        if js_hook and hasattr(window, 'browser') :
            print('[webview2][事件] edge 添加js_hook')
            setattr(window.browser, 'js_hook', js_hook_outer)

    window.events.closed += wvOnClosed
    window.events.loaded += wvOnDomLoad
    window.events.shown += wvOnShow
    webview.start(wvOnLoad, window, debug=debug)