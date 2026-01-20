@echo off
echo.
echo ========================================
echo   CI/CD Pipeline - Registration App
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [Step 1/5] Running tests...
echo.
python tests\test_validation.py
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   TESTS FAILED! Fix your code!
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   All tests passed!
echo ========================================
echo.

echo [Step 2/5] Building Docker image...
echo.
docker build -t registration-app:latest .
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   Docker build failed!
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo.
echo  Docker image built successfully!
echo.

echo [Step 3/5] Stopping old container...
echo.
docker stop registration-app 2>nul
docker rm registration-app 2>nul
echo  Old container removed
echo.

echo [Step 4/5] Starting new container...
echo.
docker run -d -p 8501:8501 --name registration-app registration-app:latest
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo    Container start failed!
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo Container started!
echo.

echo [Step 5/5] Verifying deployment...
echo.
timeout /t 3 /nobreak > nul
docker ps --filter "name=registration-app"

echo.
echo ========================================
echo   CI/CD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Tests: PASSED
echo Docker: BUILT
echo Deployed: http://localhost:8501
echo.
echo ========================================
echo.
echo Opening app in browser in 3 seconds...
timeout /t 3 /nobreak > nul
start http://localhost:8501