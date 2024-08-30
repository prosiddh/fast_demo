@echo off
echo Installing required packages...
pip install -r requirements.txt

echo Starting the server...
uvicorn app_demo.main:app --port 8005

pause
