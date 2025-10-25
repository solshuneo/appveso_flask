import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Lấy chuỗi kết nối từ biến môi trường (Vercel tự động nạp .env)
DATABASE_URL = os.environ.get('DATABASE_URL')

# --- Cực kỳ quan trọng ---
# SQLAlchemy cần biết driver bạn đang dùng. 
# Vercel dùng 'psycopg2-binary', nên ta cần đổi 'postgresql://'
# thành 'postgresql+psycopg2://'
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
# -------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 1. ĐỊNH NGHĨA MODEL (BẢNG)
# Định nghĩa bảng 'user' với hai cột 'phone' và 'name'
class User(db.Model):
    # Đặt tên bảng rõ ràng (tùy chọn nhưng nên có)
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Tạo một route gốc
@app.route("/")
def index():
    return "<h1>Chào mừng!</h1><p>Hãy truy cập <b>/home</b> để kiểm tra database Neon.</p>"

# 2. TẠO ROUTE /home
@app.route("/home")
def home():
    output_html = "<h1>Test Vercel + Neon DB</h1>"
    
    try:
        # Đảm bảo app context được kích hoạt
        with app.app_context():
            # 3. TẠO BẢNG
            # Lệnh này sẽ tạo bảng 'users' nếu nó chưa tồn tại
            db.create_all()
            output_html += "<p>Đã kiểm tra/tạo bảng 'users' thành công.</p>"

            # 4. THÊM THÔNG TIN (chỉ thêm nếu bảng rỗng)
            if User.query.count() == 0:
                output_html += "<p>Bảng rỗng. Đang thêm dữ liệu mẫu...</p>"
                # Tạo một user mẫu
                sample_user = User(phone="0905123456", name="Người Dùng Test")
                db.session.add(sample_user)
                db.session.commit()
                output_html += "<p>Đã thêm: SĐT: 0905123456, Tên: Người Dùng Test</p>"
            else:
                 output_html += "<p>Bảng đã có dữ liệu. Bỏ qua bước thêm mẫu.</p>"

            # 5. LẤY THÔNG TIN RA
            output_html += "<h2>Dữ liệu hiện tại trong bảng 'users':</h2>"
            
            # Lấy tất cả user từ database
            all_users = User.query.all()
            
            if not all_users:
                output_html += "<p>Không tìm thấy user nào.</p>"
            else:
                # Hiển thị theo yêu cầu: "lấy sđt ra tên"
                for user in all_users:
                    output_html += f"<p><b>SĐT:</b> {user.phone} &rarr; <b>Tên:</b> {user.name}</p>"

    except Exception as e:
        # Hiển thị lỗi nếu kết nối hoặc truy vấn thất bại
        output_html += f"<h2 style='color: red;'>ĐÃ XẢY RA LỖI:</h2>"
        output_html += f"<pre>{e}</pre>"
        output_html += "<p><i>(Kiểm tra lại DATABASE_URL trong Cài đặt Project trên Vercel)</i></p>"

    return output_html