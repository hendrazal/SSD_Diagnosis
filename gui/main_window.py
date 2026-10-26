import tkinter as tk

from gui.input_page import InputPage
from gui.dataset_page import DatasetPage
from gui.result_page import ResultPage
from gui.visualization_page import VisualizationPage

class MainWindow(tk.Frame):
    """
    Layout pembungkus utama aplikasi.
    Container konten utama dengan title bar sesuai mockup HTML tanpa sidebar.
    """

    def __init__(self, parent_controller):
        super().__init__(parent_controller)
        self.controller = parent_controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_main_area()

    def create_main_area(self):
        """
        Membuat layout area utama: Title Bar di baris 0, Top Bar di baris 1, Container Halaman di baris 2.
        """
        main_area = tk.Frame(self, bg="#F5F6FA")
        main_area.grid(row=0, column=0, sticky="nsew")
        main_area.columnconfigure(0, weight=1)
        main_area.rowconfigure(0, weight=0)
        main_area.rowconfigure(1, weight=1)

        title_bar = tk.Frame(main_area, bg="#185fa5", height=34)
        title_bar.grid(row=0, column=0, sticky="ew")
        title_bar.grid_propagate(False)

        title_text = tk.Label(
            title_bar,
            text="Sistem Diagnosis SSD v1.0",
            font=("Arial", 10, "bold"),
            bg="#185fa5",
            fg="#d0e4ff"
        )
        title_text.pack(side="left", padx=14, pady=8)

        self.container = tk.Frame(main_area, bg="#F5F6FA")
        self.container.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 8))
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}

        for PageClass in (InputPage, DatasetPage, ResultPage, VisualizationPage):
            page_name = PageClass.__name__
            page_instance = PageClass(parent_container=self.container, controller=self.controller)
            self.pages[page_name] = page_instance
            
            page_instance.grid(row=0, column=0, sticky="nsew")

        self.current_page = "InputPage"
        self.show_page("InputPage")

    def show_page(self, page_class_name):
        """
        Menampilkan halaman yang dipilih di atas halaman lainnya.
        """
        page = self.pages[page_class_name]
        if hasattr(page, "on_show_page"):
            page.on_show_page()

        page.tkraise()
        self.current_page = page_class_name
