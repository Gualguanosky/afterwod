@echo off
title Militar Box Launcher
echo Iniciando Militar Box Afterwod...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error al abrir la aplicacion.
    echo Asegurate de tener Python y las dependencias instaladas.
    pause
)
