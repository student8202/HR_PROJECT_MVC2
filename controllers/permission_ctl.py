from database import get_db_connection

class PermissionController:
    @staticmethod
    def get_view_rights(employee_id):
        """Lấy danh sách ID bộ phận mà nhân viên được phép xem"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DeptID FROM EmployeeViewRights WHERE EmployeeID = ?", (employee_id,))
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def update_view_rights(employee_id, dept_ids):
        """Cập nhật quyền xem bộ phận (Xóa cũ, thêm mới)"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # 1. Xóa quyền cũ
            cursor.execute("DELETE FROM EmployeeViewRights WHERE EmployeeID = ?", (employee_id,))
            # 2. Thêm quyền mới
            if dept_ids and len(dept_ids) > 0:
                params = [(employee_id, d_id) for d_id in dept_ids]
                cursor.executemany("INSERT INTO EmployeeViewRights (EmployeeID, DeptID) VALUES (?, ?)", params)
            conn.commit()
            return True