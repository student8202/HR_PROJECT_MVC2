@echo off
:: Lấy thời gian
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /format:list') do set datetime=%%I
set ts=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%:%datetime:~10,2%:%datetime:~12,2%
echo [%ts%] Dang kiem tra va khoi dong lai...
cd /d "C:\SMILE PMS\HR_PROJECT_MVC2"
"C:\Program Files\Python312\python.exe" -m pip install flask waitress --user
"C:\Program Files\Python312\python.exe" -m pip install pyodbc --user
"C:\Program Files\Python312\python.exe" -m pip install pandas openpyxl --user
"C:\Program Files\Python312\python.exe" app.py
pause