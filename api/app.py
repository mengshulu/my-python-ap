# from flask import Flask   # 載入 Flask
#
# app = Flask(__name__)     # 建立 app 變數為 Flask 物件，__name__ 表示目前執行的程式
#
# @app.route("/")           # 使用函式裝飾器，建立一個路由 ( Routes )，可針對主網域 / 發出請求
# def home():               # 發出請求後會執行 home() 的函式
#     return "<h1>hello world</h1>"   # 執行函式後會回傳特定的網頁內容
#
# app.run()                 # 執行

from flask import Flask, request, Blueprint

app = Flask(__name__)
api = Blueprint('api', __name__)

@api.route("/", methods=['GET'])
def home():
    print("fff")
    return "<h1>hello world</h1>"

@api.route("/ok")
def ok():

    print(request.args)            # 使用 request.args
    return "<h1>ok</h1>"

@api.route("/yes")
def yes():
    return "<h1>yes</h1>"

@api.route("/fail")
def fail():
    return "<h1>fail</h1>"

@api.route("/hello")
def hello():
    print("hello")
    response = {"message": "Hello from Python API on Vercel!"}
    return response

# @app.route("/<msg>")           # 加入 <msg> 讀取網址
# def ok(msg):                   # 加入參數
#     return f"<h1>{msg}</h1>"   # 使用變數
#
# @app.route("/<path:msg>")     # 加入 path: 轉換成「路徑」的類型
# def ok(msg):
#     return f"<h1>{msg}</h1>"

# app.run()
# app.run(host="0.0.0.0", port=5555)
app.register_blueprint(api, url_prefix='/api')
if __name__ == "__main__":
    app.run(debug=True)