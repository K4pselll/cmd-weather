@echo off
if "%PYTHON%"=="" (
    set "PYTHON=py"
)
"%PYTHON%" "%~dp0\Main.py" %*
