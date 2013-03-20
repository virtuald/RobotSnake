@echo off

REM location of run_test.py relative to this file
set FAKE_WPILIB_DIR=fake-wpilib

REM location of test modules relative to this file
set TEST_MODULES=launchers


set ec=1

set PYTHON_EXE=python.exe

REM TODO: Need a better way to detect python 3 automatically

set PYTHON_BIN=C:\Python32\%PYTHON_EXE%
if exist %PYTHON_BIN% goto python_found

set PYTHON_BIN=C:\Python33\%PYTHON_EXE%
if exist %PYTHON_BIN% goto python_found

echo Error: Could not find python 3
exit /b 1

:python_found
%PYTHON_BIN% -B "%~dp0\%FAKE_WPILIB_DIR%\run_test.py" --test-modules="%~dp0\%TEST_MODULES%" %*

if "%errorlevel%" == "0" set ec=0
pause

exit /b %ec%
