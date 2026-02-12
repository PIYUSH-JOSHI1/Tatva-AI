@echo off
REM Quick Start Script for Tatva AI Hospital Management System

echo ========================================
echo  Tatva AI - Hospital Management System
echo ========================================
echo.

echo Checking environment...
python --version
echo.

echo Starting Streamlit application...
echo.
echo Opening in browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run Hospital_Streamlit.py
