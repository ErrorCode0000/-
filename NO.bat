@echo off
setlocal EnableDelayedExpansion
title Dosya/Klasor Silme Araci

:: Yonetici yetkisi kontrolu
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Administrator yetkisi gerekli!
    echo Lutfen bu dosyayi yonetici olarak calistirin.
    pause
    exit /B 1
)

:: Kullanicidan yol al
set /p "targetPath=Silinecek dosya/klasor yolunu girin: "

echo.
echo Silme islemi basliyor: %targetPath%
echo.

:: TrustedInstaller servisini durdur
net stop TrustedInstaller /y >nul 2>&1

:: System yetkilerini kaldir
echo Sistem yetkileri kaldiriliyor...
icacls "%targetPath%" /setowner "Administrators" /T /C >nul 2>&1
icacls "%targetPath%" /reset /T >nul 2>&1

:: Tum yetkileri al
echo Yetkiler aliniyor...
takeown /F "%targetPath%" /A /R /D Y >nul 2>&1
icacls "%targetPath%" /grant:r Administrators:F /T /C /Q >nul 2>&1
icacls "%targetPath%" /grant:r %username%:F /T /C /Q >nul 2>&1

:: Dosya/Klasor kontrolu
if exist "%targetPath%\*" (
    :: Klasor ise
    echo Klasor siliniyor...
    rd /s /q "%targetPath%" 2>nul
    if exist "%targetPath%" (
        :: Eger hala duruyorsa, force ile dene
        echo Normal silme basarisiz. Force kullaniliyor...
        rmdir /s /q "%targetPath%" 2>nul
        if exist "%targetPath%" (
            echo Force silme de basarisiz. Del komutu deneniyor...
            del /f /s /q "%targetPath%\*" >nul 2>&1
            rmdir /s /q "%targetPath%" >nul 2>&1
        )
    )
) else (
    :: Dosya ise
    echo Dosya siliniyor...
    del /f /q "%targetPath%" 2>nul
)

:: Son kontrol
if exist "%targetPath%" (
    echo.
    echo HATA: Silme islemi basarisiz oldu!
    echo Lutfen Windows Guvenli Modda tekrar deneyin.
    echo.
) else (
    echo.
    echo BASARILI: Silme islemi tamamlandi!
    echo.
)

:: TrustedInstaller servisini tekrar baslat
net start TrustedInstaller >nul 2>&1

pause
exit /B 0
