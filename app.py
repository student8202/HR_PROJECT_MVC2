from flask import Flask, render_template, session, redirect, url_for
from views.employee_view import employee_bp
from views.department_view import department_bp 
from views.auth_view import auth_bp # Import thêm Blueprint Auth
from waitress import serve
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = "hr_pro_key"

# --- CHỈNH SỬA ROUTE GỐC ---
@app.route('/')
def index():
    # Nếu chưa có user_id trong session, bắt quay về trang login
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    return render_template('index.html')

# --- ĐĂNG KÝ CÁC BLUEPRINT ---
app.register_blueprint(auth_bp) # Đăng ký Auth trước
app.register_blueprint(employee_bp)
app.register_blueprint(department_bp)

app.config['DEBUG'] = True

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6066))
    print(f"SMILE HR MVC2 Service is running on port {port}...")
    serve(app, host='127.0.0.1', port=port)