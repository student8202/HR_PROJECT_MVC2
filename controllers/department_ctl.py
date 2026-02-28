from database import get_db_connection

class DepartmentController:
    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Departments")
            return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    @staticmethod
    def save(data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            dept_name = data.get('DeptName', '').strip()
            dept_id = data.get('DeptID')

            # 1. Kiểm tra trùng tên (Loại trừ chính nó nếu là đang Sửa)
            if dept_id: # Trường hợp Sửa
                cursor.execute("SELECT COUNT(*) FROM Departments WHERE DeptName = ? AND DeptID != ?", (dept_name, dept_id))
            else: # Trường hợp Thêm mới
                cursor.execute("SELECT COUNT(*) FROM Departments WHERE DeptName = ?", (dept_name,))
            
            if cursor.fetchone()[0] > 0:
                return False, "err_dept_exists" # Trả về key ngôn ngữ để JS dịch

            # 2. Thực hiện Lưu/Cập nhật
            if dept_id:
                cursor.execute("UPDATE Departments SET DeptName=? WHERE DeptID=?", (dept_name, dept_id))
            else:
                cursor.execute("INSERT INTO Departments (DeptName) VALUES (?)", (dept_name,))
            
            conn.commit()
            return True, "save_success"

    @staticmethod
    def delete(dept_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # BƯỚC 1: Kiểm tra xem có nhân viên nào thuộc bộ phận này không
            cursor.execute("SELECT COUNT(*) FROM Employees WHERE IdDepartment = ?", (dept_id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                # Trả về False hoặc báo lỗi nếu còn nhân viên
                return False, f"Không thể xóa! Đang có {count} nhân viên thuộc bộ phận này."
            
            # BƯỚC 2: Nếu không có nhân viên, tiến hành xóa
            cursor.execute("DELETE FROM Departments WHERE DeptID = ?", (dept_id,))
            conn.commit()
            return True, "Xóa bộ phận thành công."