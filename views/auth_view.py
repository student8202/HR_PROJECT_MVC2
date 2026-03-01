from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from controllers.auth_ctl import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login_page():
    # Nếu đã đăng nhập rồi thì vào thẳng index
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    result = AuthController.login(data.get('username'), data.get('password'))
    
    if result["status"] == "success":
        # Lưu vào Session Server để bảo mật route '/'
        session['user_id'] = result["user"]["id"]
        session['permissions'] = result["user"]["perms"]
    
    return jsonify(result)

@auth_bp.route('/api/logout')
def api_logout():
    session.clear()
    return jsonify({"status": "success"})