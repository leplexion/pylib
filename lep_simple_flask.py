from flask import Flask, request
import json
import requests

def post2flask(port:int, data:dict):
    try:
        res = requests.post(f'http://127.0.0.1:{port}', json=data)
        return res
    except Exception as e:
        print(f'post2flask输出错误, 错误类型{type(e).__name__}')
        return None

# def flaskexit():
#     shutdownfn = request.environ.get('werkzeug.server.shutdown')
#     if shutdownfn is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     shutdownfn()

def lep_simple_flask_json(cb, port:int):
    app = Flask(__name__)

    @app.before_request
    def before_request():
        if not request.data:
            res = cb(None)
        else:
            req = request.data.decode('utf-8')            
            req = json.loads(req)
            res = cb(req)

        if type(res).__name__ == 'dict':
            return json.dumps(res), 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*'}
        else:
            return str(res), 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*'}

    app.run('0.0.0.0', port, debug=False)



