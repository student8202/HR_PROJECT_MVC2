from database import get_db_connection
import pandas as pd
from io import BytesIO


class EmployeeController:
    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT E.ID, E.FullName, D.DeptName, E.IdDepartment 
                FROM Employees E LEFT JOIN Departments D ON E.IdDepartment = D.DeptID
            """
            )
            return [
                dict(zip([col[0] for col in cursor.description], row))
                for row in cursor.fetchall()
            ]

    @staticmethod
    def save(data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                if data.get("ID"):
                    # Trường hợp SỬA
                    cursor.execute(
                        "UPDATE Employees SET FullName=?, IdDepartment=? WHERE ID=?",
                        (data["FullName"], data["IdDepartment"], data["ID"]),
                    )
                    conn.commit()
                    return data["ID"]
                else:
                    # Trường hợp THÊM MỚI (Dùng SET NOCOUNT ON để tránh lỗi 500)
                    sql = """
                        SET NOCOUNT ON;
                        INSERT INTO Employees (FullName, IdDepartment) VALUES (?, ?);
                        SELECT CAST(SCOPE_IDENTITY() AS INT);
                    """
                    cursor.execute(sql, (data["FullName"], data["IdDepartment"]))
                    
                    # Lấy ID vừa tạo
                    new_id_row = cursor.fetchone()
                    new_id = new_id_row[0] if new_id_row else None
                    
                    conn.commit()
                    return new_id
            except Exception as e:
                conn.rollback() # Hoàn tác nếu lỗi
                print(f"Database Error: {str(e)}") # Xem lỗi tại terminal
                raise e # Đẩy lỗi ra để View bắt được

    @staticmethod
    def delete(id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Employees WHERE ID=?", (id,))
            conn.commit()

    @staticmethod
    def get_template_excel():
        # 1. Lấy danh sách phòng ban thực tế từ DB để hướng dẫn người dùng
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DeptName FROM Departments")
            departments = [row.DeptName for row in cursor.fetchall()]

        # 2. Tạo DataFrame mẫu với dữ liệu ví dụ
        df_template = pd.DataFrame(
            {
                "FullName": ["Nguyễn Văn A", "Trần Thị B"],
                "DepartmentName": (
                    departments[:2] if departments else ["Phòng IT", "Phòng Kế Toán"]
                ),
            }
        )

        # 3. Xuất ra file Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_template.to_excel(writer, index=False, sheet_name="Import_Template")

            # (Tùy chọn) Thêm một sheet hướng dẫn danh sách phòng ban hợp lệ
            if departments:
                df_depts = pd.DataFrame({"Danh sách Phòng ban hợp lệ": departments})
                df_depts.to_excel(writer, index=False, sheet_name="Valid_Departments")

        output.seek(0)
        return output

    @staticmethod
    def import_excel(file):
        try:
            # 1. Đọc file Excel
            df = pd.read_excel(file)

            # 2. Lấy danh sách Department hiện tại để ánh xạ (Mapping)
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DeptID, DeptName FROM Departments")
                # Tạo dictionary { 'Phòng IT': 1, 'Phòng Nhân sự': 2 }
                dept_map = {row.DeptName: row.DeptID for row in cursor.fetchall()}

            # 3. Chuẩn bị dữ liệu để chèn
            # Giả sử file Excel có cột: "FullName" và "DepartmentName"
            import_data = []
            for _, row in df.iterrows():
                full_name = row.get("FullName")
                dept_name = row.get("DepartmentName")  # Tên phòng ban từ Excel

                # Tìm ID tương ứng từ map, nếu không thấy thì để None
                dept_id = dept_map.get(dept_name)

                import_data.append((full_name, dept_name, dept_id))

            # 4. Thực hiện Bulk Insert
            with get_db_connection() as conn:
                cursor = conn.cursor()
                sql = """
                        INSERT INTO Employees (FullName, Department, IdDepartment) 
                        VALUES (?, ?, ?)
                    """
                cursor.executemany(sql, import_data)
                conn.commit()

            return len(import_data)
        except Exception as e:
            raise Exception(f"Lỗi logic Import: {str(e)}")

    @staticmethod
    def export_excel():
        # Lấy dữ liệu đầy đủ từ DB
        data = EmployeeController.get_all()
        # Chuyển sang DataFrame và đặt tên cột cho file Excel đẹp hơn
        df = pd.DataFrame(data)
        df_export = df.rename(
            columns={"FullName": "Họ và Tên", "DeptName": "Phòng Ban", "ID": "Mã NV"}
        )[["Mã NV", "Họ và Tên", "Phòng Ban"]]

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_export.to_excel(writer, index=False, sheet_name="Danh_sach_NV")
        output.seek(0)
        return output
