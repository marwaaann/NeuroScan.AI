@echo off
echo ========================================================
echo   Nuroscan - AI Brain Health Screening Platform
echo ========================================================
echo.
echo 1. Starting FastAPI Backend (Port 8000)...
start "Nuroscan FastAPI Backend" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

echo 2. Waiting for backend initialization...
timeout /t 3 /nobreak >nul

echo 3. Starting Streamlit Frontend (Port 8501)...
start "Nuroscan Streamlit Frontend" cmd /k "python -m streamlit run frontend/app.py --server.port 8501"

echo.
echo ========================================================
echo   Backend API:   http://127.0.0.1:8000/docs
echo   Frontend App:  http://localhost:8501
echo ========================================================
echo.
pause
