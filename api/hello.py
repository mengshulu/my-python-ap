from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 設置響應頭
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # 返回 JSON 數據
        response = {"message": "Hello from Python API on Vercel!"}
        self.wfile.write(json.dumps(response).encode("utf-8"))
