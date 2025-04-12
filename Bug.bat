@echo off
echo Güvenlik güncellemeleri kaldırılıyor...

:: MS17-010 (EternalBlue) ile ilgili güncellemeleri kaldır
wusa /uninstall /kb:4013389 /quiet /norestart
wusa /uninstall /kb:4012212 /quiet /norestart
wusa /uninstall /kb:4012598 /quiet /norestart

:: SMBGhost (CVE-2020-0796) ile ilgili güncellemeleri kaldır
wusa /uninstall /kb:4551762 /quiet /norestart
wusa /uninstall /kb:4550945 /quiet /norestart

echo Güvenlik güncellemeleri kaldırıldı. Lütfen sistemi yeniden başlatın.
pause
