python -m venv venv
echo "Virtual Environment Created"
pause

call venv\Scripts\activate
echo "Virtual Environment Activated"
pause

pip install -r requirements.txt
echo "Required Packages Installed"

echo "Removing log files..."
del /s /q *.log
echo "Log files removed!!"
pause

echo "Expense Batch Migration Started"
call python main.py
echo "Expense Batch Migration Completed!!"

call venv\Scripts\deactivate.bat
echo "Virtual Environment Deactivated"

rmdir /s /q venv
echo "Virtual Environment Deleted"
pause

echo "Deleting __pycache__ folders..."
for /r %%i in (__pycache__) do (
    if exist "%%i" (
        rmdir /s /q "%%i"
    )
)
echo "__pycache__ folders deleted!!"
pause