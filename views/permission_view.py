from flask import Blueprint, request, jsonify
from controllers.permission_ctl import PermissionController

perm_bp = Blueprint('perm', __name__)

@perm_bp.route('/api/permissions/view-list', methods=['GET'])
def get_view_list():
    return jsonify(PermissionController.get_all_with_view_rights())

@perm_bp.route('/api/permissions/view-rights/<int:emp_id>', methods=['GET'])
def get_emp_rights(emp_id):
    return jsonify(PermissionController.get_view_rights_by_emp(emp_id))

@perm_bp.route('/api/permissions/save-view-rights', methods=['POST'])
def save_rights():
    data = request.json
    PermissionController.save_view_rights(data['employee_id'], data['dept_ids'])
    return jsonify({"status": "success"})