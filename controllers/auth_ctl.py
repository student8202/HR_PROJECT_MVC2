from database import get_db_connection

class AuthController:
    @staticmethod
    def login(username, password):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Truy vấn khớp với Database hiện tại của bạn
            cursor.execute("""
                SELECT ID, FullName, Permissions 
                FROM Employees 
                WHERE FullName = ? AND Password = ?
            """, (username, password))
            user = cursor.fetchone()
            
            if user:
                return {
                    "status": "success",
                    "user": {
                        "id": user.ID,
                        "name": user.FullName,
                        "perms": user.Permissions if user.Permissions else ""
                    }
                }
            return {"status": "error", "message": "Tài khoản hoặc mật khẩu không đúng!"}