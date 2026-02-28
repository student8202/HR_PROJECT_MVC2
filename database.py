import pyodbc

def get_db_connection():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;DATABASE=SMILE_HR;UID=smile;PWD=AnhMinh167TruongDinh;'
    )
    return pyodbc.connect(conn_str)