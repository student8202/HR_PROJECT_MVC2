from flask import Blueprint, jsonify, request
from controllers.department_ctl import DepartmentController

department_bp = Blueprint('department', __name__)

@department_bp.route('/api/departments', methods=['GET'])
def get_depts(): return jsonify(DepartmentController.get_all())

@department_bp.route('/api/departments/save', methods=['POST'])
def save_dept():
    success, message_key = DepartmentController.save(request.json)
    if success:
        return jsonify({"status": "success", "message": message_key}), 200
    else:
        # Trả về lỗi 400 (Bad Request) nếu trùng tên
        return jsonify({"status": "error", "message": message_key}), 400

@department_bp.route('/api/departments/delete/<int:id>', methods=['DELETE'])
def del_dept(id):
    success, message = DepartmentController.delete(id)
    if success:
        return jsonify({"status": "success", "message": message}), 200
    else:
        # Trả về lỗi 400 kèm tin nhắn cảnh báo
        return jsonify({"status": "error", "message": message}), 400