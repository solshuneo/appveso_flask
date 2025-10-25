from flask import Flask, request, jsonify
import json

# Khởi tạo ứng dụng Flask
# Vercel sẽ tự động tìm biến tên 'app' này
app = Flask(__name__)
@app.route("/", methods=['GET'])
def home():
    return "welcome!"