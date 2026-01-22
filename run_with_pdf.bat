@echo off
chcp 65001 >nul
echo PDF to CSV Converter
echo ====================
echo.
echo Enter PDF file name (e.g., 001.pdf, 002.pdf):
set /p PDFNAME="PDF file: "
python process_pdf_complete.py %PDFNAME%
pause
