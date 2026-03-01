from flask import Blueprint, request, jsonify
from controllers.permission_ctl import PermissionController

perm_bp = Blueprint('permission', __name__)

@perm_bp.route('/api/permissions/view-rights/<int:emp_id>', methods=['GET'])
def get_rights(emp_id):
    rights = PermissionController.get_view_rights(emp_id)
    return jsonify(rights)

@perm_bp.route('/api/permissions/view-rights', methods=['POST'])
def update_rights():
    data = request.json
    emp_id = data.get('employee_id')
    dept_ids = data.get('dept_ids') # Mảng [1, 2, 3]
    
    if PermissionController.update_view_rights(emp_id, dept_ids):
        return jsonify({"status": "success", "message": "Cập nhật quyền thành công"})
    return jsonify({"status": "error"}), 500