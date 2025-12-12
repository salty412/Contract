@echo off
REM === Deployment Script for PDF Splitter (Using EXE) ===
REM This script creates the deployment folder, copies the EXE and REG file, and sets up the BAT file.

set "TARGET_DIR=C:\CalahanTools\PDFSplitter"
set "REG_FILE=PDFSplitter.reg"
REM IMPORTANT: Ensure 'pdfsplitter.exe' is present in the source folder
set "EXE_FILE=pdfsplitter.exe" 

echo Checking if target directory exists...
if not exist "%TARGET_DIR%" (
    echo Creating directory %TARGET_DIR%
    mkdir "%TARGET_DIR%"
)

REM === 1. Copy Files (Source folder must contain pdfsplitter.exe and PDFSplitter.reg) ===
echo Copying necessary files to %TARGET_DIR%...
copy /Y "%EXE_FILE%" "%TARGET_DIR%"
copy /Y "%REG_FILE%" "%TARGET_DIR%"

if errorlevel 1 (
    echo ERROR: Failed to copy files. Please ensure %EXE_FILE% and %REG_FILE% are in the source folder. Exiting deployment.
    pause
    goto :eof
)

REM === 2. Create the simple contract.bat file (which calls the deployed EXE) ===
echo Creating the deployed contract.bat file...
(
    echo @echo off
    REM This calls the packaged executable directly
    echo "%TARGET_DIR%\%EXE_FILE%" "%%~1"
) > "%TARGET_DIR%\contract.bat"

REM === 3. Import Registry Key (Silent Import) ===
echo Importing registry settings for the current user...
reg import "%TARGET_DIR%\%REG_FILE%" /reg:32 /reg:64 /y

if errorlevel 1 (
    echo ERROR: Failed to import registry key.
    echo Check permissions (must be run as user or with admin rights if deploying to HKCU).
    pause
) else (
    echo Deployment successful!
)

echo Deployment complete.
pause