import tkinter as tk
from tkinter import messagebox
import os
import sys

# Menambahkan direktori proyek ke sys.path agar modul lokal dapat diimpor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import WINDOW_TITLE, WINDOW_SIZE
from gui.main_window import MainWindow

class SistemDiagnosisApp(tk.Tk):
    """
    Kelas utama aplikasi Sistem Diagnosis SSD.
    Mengatur siklus hidup aplikasi, inisialisasi jendela utama Tkinter,
    dan penyimpanan data hasil diagnosis sementara.
    """

    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(1020, 650)
        self.configure(bg="#F5F6FA")

        # Variabel untuk menampung data hasil prediksi terakhir (tanpa database)
        self.shared_data = {
            "last_prediction": None
        }

        # Menginisialisasi tata letak utama (Sidebar & Konten Utama)
        self.main_window = MainWindow(self)
        self.main_window.pack(fill="both", expand=True)

    def show_page(self, page_class_name):
        """
        Berfungsi untuk memicu perpindahan halaman pada area konten utama.
        """
        self.main_window.show_page(page_class_name)

    def set_shared_data(self, key, value):
        """
        Menyimpan data yang dapat diakses antar halaman.
        """
        self.shared_data[key] = value

    def get_shared_data(self, key):
        """
        Mengambil data bersama berdasarkan kunci tertentu.
        """
        return self.shared_data.get(key)


if __name__ == "__main__":
    # Menjalankan aplikasi
    app = SistemDiagnosisApp()
    app.mainloop()
