# from flask import Flask   # 載入 Flask
#
# app = Flask(__name__)     # 建立 app 變數為 Flask 物件，__name__ 表示目前執行的程式
#
# @app.route("/")           # 使用函式裝飾器，建立一個路由 ( Routes )，可針對主網域 / 發出請求
# def home():               # 發出請求後會執行 home() 的函式
#     return "<h1>hello world</h1>"   # 執行函式後會回傳特定的網頁內容
#
# app.run()                 # 執行

import os

from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, request, Blueprint, jsonify
from flask_cors import CORS

app = Flask(__name__)
api = Blueprint('api', __name__)
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://thunderous-chimera-ad54f4.netlify.app/",
        "http://127.0.0.1:3005/"
    ]
}})
load_dotenv()
# 連接到 MongoDB
app.config["MONGO_URI"] = os.getenv("MONGODB_URI")
client = MongoClient(app.config["MONGO_URI"])
db = client.sample_mflix  # 獲取 sample_mflix 資料庫
# print(db.movies.find_one({'title': 'Parasite'}))

@api.route("/", methods=['GET'])
def home():
    return "<h1>hello world</h1>"

@api.route("/movies", methods=['POST'])
def get_movies():
    # movie = db.movies.find_one({'title': 'Parasite'})
    # movie['_id'] = str(movie['_id'])

    # movies = db.movies.find() 一直出現下面的問題
    # BrokenPipeError: [Errno 32] Broken pipe是一個常見的錯誤，通常出現在伺服器端嘗試向客戶端寫入數據時，而客戶端已經關閉了連接。這種情況在網絡編程中是相對正常的，特別是當客戶端在伺服器完成響應之前就終止了連接。
    # 推斷應該是因為這個表有 2 萬多筆資料，改成只取 10筆就好了

    # 從請求中獲取 JSON 載荷
    data = request.get_json()

    # 檢查必要的參數是否存在
    if 'page_number' not in data:
        return {'message': 'Missing parameters page_number'}, 400
    elif 'page_size' not in data or data['page_size'] > 20:
        return {'message': 'page_size not Valid'}, 400

    # 獲取參數
    # 設置分頁參數
    page_number = data['page_number']  # 第一頁
    page_size = data.get('page_size', 10)   # 每頁顯示 10 筆
    #
    # # 計算跳過的文檔數
    skip = (page_number - 1) * page_size

    movies = db.movies.find().skip(skip).limit(page_size)  # 從 'movies' 集合中獲取所有文檔
    movies_list = []
    for movie in movies:
        movie['_id'] = str(movie['_id'])  # 將 ObjectId 轉換為字符串
        movies_list.append(movie)
    return jsonify(movies_list)

@api.route("/ok")
def ok():

    # print(request.args)            # 使用 request.args
    return "<h1>ok</h1>"

@api.route("/yes")
def yes():
    return "<h1>yes</h1>"

@api.route("/fail")
def fail():
    return "<h1>fail</h1>"

@api.route("/hello")
def hello():
    # print("hello")
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