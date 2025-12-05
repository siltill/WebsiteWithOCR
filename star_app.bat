@echo off
title Starting OCR app

echo Start Backend...
start "Backend" cmd /k "cd backend && go run main.go"

echo Start Frontend...
start "Frontend" cmd /k "cd frontend\ocr_app_frontend\ && npm run dev"

echo All work!
pause
