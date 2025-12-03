@echo off
echo =====================================
echo Phase 1: Environment Setup
echo =====================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo Step 1: Creating Python Virtual Environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating Virtual Environment...
call venv\Scripts\activate.bat

echo Step 3: Installing Dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo =====================================
echo Phase 1 Complete!
echo =====================================
echo.
echo Next Steps:
echo 1. Configure AWS credentials by running: aws configure
echo 2. Copy your AWS credentials from Udacity Cloud Lab:
echo    - Access Key ID
echo    - Secret Access Key
echo    - Region: us-east-1
echo    - Format: json
echo.
echo 3. IMPORTANT: Add session token manually!
echo    - Run: notepad %%USERPROFILE%%\.aws\credentials
echo    - Add this line under [default]:
echo      aws_session_token = YOUR_SESSION_TOKEN_HERE
echo.
echo 4. Verify connectivity: aws sts get-caller-identity
echo.
pause
