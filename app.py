from flask import Flask,render_template
from views.employee_view import employee_bp
from views.department_view import department_bp 
from waitress import serve
import os


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = "hr_pro_key"

# --- THÊM ĐOẠN NÀY ---
@app.route('/')
def index():
    return render_template('index.html')
# ---------------------
app.register_blueprint(employee_bp)
app.register_blueprint(department_bp)

app.config['DEBUG'] = True

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6066))
    print(f"SMILE HR MVC2 Service is running on port {port}...")
    serve(app, host='127.0.0.1', port=port)