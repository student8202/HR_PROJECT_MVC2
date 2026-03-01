from database import get_db_connection

class PermissionController:
    @staticmethod
    def get_all_with_view_rights():
        """Lấy danh sách NV kèm chuỗi tên bộ phận được xem"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT e.ID, e.FullName, 
                STUFF((SELECT ', ' + d.DeptName 
                       FROM EmployeeViewRights evr 
                       JOIN Departments d ON evr.DeptID = d.DeptID 
                       WHERE evr.EmployeeID = e.ID 
                       FOR XML PATH('')), 1, 2, '') AS ViewDepts
                FROM Employees e
            """
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_view_rights_by_emp(emp_id):
        """Lấy mảng ID bộ phận để đổ vào Select2"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DeptID FROM EmployeeViewRights WHERE EmployeeID = ?", (emp_id,))
            return [row[0] for row in cursor.fetchall()] 

    @staticmethod
    def save_view_rights(emp_id, dept_ids):
        """Cập nhật quyền: Xóa cũ, thêm mới"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM EmployeeViewRights WHERE EmployeeID = ?", (emp_id,))
            if dept_ids:
                params = [(emp_id, int(d_id)) for d_id in dept_ids]
                cursor.executemany("INSERT INTO EmployeeViewRights (EmployeeID, DeptID) VALUES (?, ?)", params)
            conn.commit()
            return True