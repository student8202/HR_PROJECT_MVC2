from flask import Blueprint, jsonify, request
from controllers.employee_ctl import EmployeeController

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/api/employees', methods=['GET'])
def get_emps(): return jsonify(EmployeeController.get_all())

@employee_bp.route('/api/employees/save', methods=['POST'])
def save_emp():
    EmployeeController.save(request.json)
    return jsonify({"status": "success"})

@employee_bp.route('/api/employees/delete/<int:id>', methods=['DELETE'])
def del_emp(id):
    EmployeeController.delete(id)
    return jsonify({"status": "success"})