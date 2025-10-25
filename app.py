import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

# Khởi tạo ứng dụng Flask
# Vercel sẽ tự động tìm biến tên 'app' này
app = Flask(__name__)

# --- 1. CONFIG DATABASE ---
# Lấy chuỗi kết nối từ biến môi trường của Vercel
# **THAY ĐỔI Ở ĐÂY:** Lấy đúng tên biến từ Vercel (theo ảnh chụp của bạn)
DATABASE_URL = os.environ.get('NEON_DATABASE_URL_DATABASE_URL')

# Quan trọng: Sửa đổi chuỗi kết nối cho SQLAlchemy
# Vercel/Neon cung cấp 'postgresql://'
# SQLAlchemy cần 'postgresql+psycopg2://'
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 2. ĐỊNH NGHĨA MODEL (BẢNG) ---
# Tạo một model cho bảng 'users'
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# --- 3. CÁC ROUTE (ĐIỀU HƯỚNG) ---

# Route gốc của bạn
@app.route("/", methods=['GET'])
def home():
    return "welcome!"

# Route mới để test database
@app.route("/testdb", methods=['GET'])
def test_db():
    output_html = "<h1>Kiểm tra kết nối Neon DB</h1>"
    
    try:
        # Sử dụng app_context để đảm bảo SQLAlchemy hoạt động
        with app.app_context():
            # 1. XÓA TẤT CẢ CÁC BẢNG (Theo yêu cầu)
            # Cảnh báo: Chỉ dùng cho test. Lệnh này sẽ xóa sạch dữ liệu.
            db.drop_all()
            output_html += "<p style='color: orange;'><b>Cảnh báo:</b> Đã chạy db.drop_all() - Xóa tất cả bảng.</p>"

            # 2. Tạo bảng (nếu chưa tồn tại)
            db.create_all()
            output_html += "<p>Đã chạy db.create_all() - Tạo lại bảng 'users' thành công.</p>"

            # 3. Thêm dữ liệu (chỉ thêm nếu bảng rỗng)
            # Vì ta vừa drop_all nên bảng sẽ luôn rỗng ở bước này
            if User.query.count() == 0:
                output_html += "<p>Bảng rỗng. Đang thêm user mẫu...</p>"
                sample_user = User(phone="0905123456", name="Test User Neon")
                db.session.add(sample_user)
                db.session.commit()
                output_html += "<p>Đã thêm: '0905123456' - 'Test User Neon'</p>"
            else:
                output_html += "<p>Bảng đã có dữ liệu, không thêm user mẫu.</p>"

            # 4. Truy vấn và hiển thị dữ liệu
            output_html += "<h2>Dữ liệu hiện tại trong bảng 'users':</h2>"
            all_users = User.query.all()
            
            if not all_users:
                output_html += "<p>Không có user nào trong database.</p>"
            else:
                output_html += "<ul>"
                for user in all_users:
                    # Lấy sđt ra tên
                    output_html += f"<li><b>SĐT:</b> {user.phone} &rarr; <b>Tên:</b> {user.name}</li>"
                output_html += "</ul>"

    except OperationalError as e:
        output_html += f"<h3 style='color: red;'>LỖI KẾT NỐI DATABASE:</h3>"
        output_html += f"<pre>{e}</pre>"
        output_html += "<p><b>Kiểm tra lại:</b> Bạn đã thêm <b>DATABASE_URL</b> vào Environment Variables trên Vercel chưa?</p>"
    except Exception as e:
        output_html += f"<h3 style='color: red;'>LỖI CHUNG:</h3>"
        output_html += f"<pre>{e}</pre>"
        
    return output_html

