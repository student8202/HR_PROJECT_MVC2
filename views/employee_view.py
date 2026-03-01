from flask import Blueprint, jsonify, request, send_file
from controllers.employee_ctl import EmployeeController

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/api/employees', methods=['GET'])
def get_emps(): return jsonify(EmployeeController.get_all())

@employee_bp.route('/api/employees/save', methods=['POST'])
def save_employee():
    try:
        new_id = EmployeeController.save(request.json)
        # Bắt buộc trả về JSON có chứa id
        return jsonify({"status": "success", "id": new_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@employee_bp.route('/api/employees/delete/<int:id>', methods=['DELETE'])
def del_emp(id):
    EmployeeController.delete(id)
    return jsonify({"status": "success"})

# --- MỚI: TẢI FILE MẪU (TEMPLATE) ---
@employee_bp.route('/api/employees/template', methods=['GET'])
def download_template():
    try:
        excel_data = EmployeeController.get_template_excel()
        return send_file(
            excel_data,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Employee_Import_Template.xlsx'
        )
    except Exception as e:
        # Trả về lỗi nếu quá trình tạo file thất bại
        return {"error": f"Không thể tạo template: {str(e)}"}, 500

# --- MỚI: XUẤT DỮ LIỆU HIỆN TẠI (EXPORT) ---
@employee_bp.route('/api/employees/export', methods=['GET'])
def export_data():
    excel_data = EmployeeController.export_excel()
    return send_file(
        excel_data,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Employees_List.xlsx'
    )

# --- MỚI: NHẬP DỮ LIỆU TỪ FILE (IMPORT) ---
@employee_bp.route('/api/employees/import', methods=['POST'])
def import_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    try:
        count = EmployeeController.import_excel(file)
        return jsonify({"status": "success", "message": f"Đã nhập thành công {count} nhân viên."})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500