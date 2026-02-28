from database import get_db_connection

class EmployeeController:
    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT E.ID, E.FullName, D.DeptName, E.IdDepartment 
                FROM Employees E LEFT JOIN Departments D ON E.IdDepartment = D.DeptID
            """)
            return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    @staticmethod
    def save(data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if data.get('ID'):
                cursor.execute("UPDATE Employees SET FullName=?, IdDepartment=? WHERE ID=?", 
                               (data['FullName'], data['IdDepartment'], data['ID']))
            else:
                cursor.execute("INSERT INTO Employees (FullName, IdDepartment) VALUES (?, ?)", 
                               (data['FullName'], data['IdDepartment']))
            conn.commit()

    @staticmethod
    def delete(id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Employees WHERE ID=?", (id,))
            conn.commit()