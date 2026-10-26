import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import threading
import subprocess

from config import DATASET_PATH, BASE_DIR

class DatasetPage(tk.Frame):
    """
    Halaman Tambah Data Latih Baru.
    Tempat pengguna menginput parameter SMART SSD beserta status aktualnya,
    dan menyimpannya langsung ke dataset.csv serta melatih ulang model C4.5.
    """

    def __init__(self, parent_container, controller):
        super().__init__(parent_container, bg="#eef4fb")
        self.controller = controller

        self.param_labels = {
            "Reallocated_Sector_Count": "Reallocated Sector Count",
            "Hardware_ECC_Recovered": "Hardware ECC Recovered",
            "Current_Pending_Sector_Count": "Current Pending Sector Count",
            "UltraDMA_CRC_Error_Count": "UltraDMA CRC Error Count",
            "Power_On_Hours": "Power-On Hours",
            "Power_Cycle_Count": "Power Cycle Count",
            "Total_LBA_Written": "Total LBA Written",
            "Total_LBA_Read": "Total LBA Read"
        }

        self.param_keys = [
            "Reallocated_Sector_Count",
            "Hardware_ECC_Recovered",
            "Current_Pending_Sector_Count",
            "UltraDMA_CRC_Error_Count",
            "Power_On_Hours",
            "Power_Cycle_Count",
            "Total_LBA_Written",
            "Total_LBA_Read"
        ]

        self.entries = {}
        self.selected_status = tk.StringVar(value="Normal")
        self.train_status_var = tk.StringVar(value="Model Siap")
        self.create_widgets()

    def create_widgets(self):
        header_card = tk.Frame(self, bg="#FFFFFF", highlightbackground="#d5e6fb", highlightthickness=1, bd=0)
        header_card.pack(fill="x", pady=(8, 8))

        header_inner = tk.Frame(header_card, bg="#FFFFFF", padx=22, pady=12)
        header_inner.pack(fill="x")

        title_block = tk.Frame(header_inner, bg="#FFFFFF")
        title_block.pack(side="left", fill="x", expand=True)

        title_lbl = tk.Label(
            title_block,
            text="Tambah Dataset",
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            fg="#0c447c"
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            title_block,
            text="Masukkan parameter SMART SSD untuk ditambahkan ke dataset.",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#3b6f9f"
        )
        subtitle_lbl.pack(anchor="w", pady=(3, 0))

        btn_back = tk.Button(
            header_inner,
            text="Kembali",
            font=("Arial", 9, "bold"),
            bg="#FFFFFF",
            fg="#185fa5",
            bd=0,
            highlightbackground="#b5d4f4",
            highlightthickness=1,
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.controller.show_page("InputPage")
        )
        btn_back.pack(side="right", padx=(12, 0))

        body = tk.Frame(self, bg="#eef4fb")
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)
        body.rowconfigure(1, weight=0)
        body.rowconfigure(2, weight=0)

        card_frame = tk.Frame(body, bg="#FFFFFF", highlightbackground="#b5d4f4", highlightthickness=1, bd=0)
        card_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 4))

        card_frame.columnconfigure(0, weight=1)
        card_frame.rowconfigure(1, weight=1)

        accent = tk.Frame(card_frame, bg="#185fa5", height=4)
        accent.grid(row=0, column=0, sticky="ew")

        inner_frame = tk.Frame(card_frame, bg="#FFFFFF", padx=22, pady=12)
        inner_frame.grid(row=1, column=0, sticky="nsew")
        inner_frame.columnconfigure(0, weight=1)

        form_grid = tk.Frame(inner_frame, bg="#FFFFFF")
        form_grid.grid(row=0, column=0, sticky="nsew")
        form_grid.columnconfigure(0, weight=1, uniform="col")
        form_grid.columnconfigure(1, weight=0)
        form_grid.columnconfigure(2, weight=1, uniform="col")

        spacer = tk.Frame(form_grid, width=26, bg="#FFFFFF")
        spacer.grid(row=0, column=1, rowspan=4)

        for i, key in enumerate(self.param_keys):
            col = 0 if i < 4 else 2
            row = i % 4

            field_frame = tk.Frame(form_grid, bg="#FFFFFF")
            field_frame.grid(row=row, column=col, sticky="ew", pady=8)
            field_frame.columnconfigure(0, weight=1)

            lbl = tk.Label(
                field_frame,
                text=self.param_labels[key],
                font=("Arial", 10, "bold"),
                bg="#FFFFFF",
                fg="#185fa5",
                anchor="w"
            )
            lbl.grid(row=0, column=0, sticky="w", pady=(0, 3))

            entry = tk.Entry(
                field_frame,
                font=("Arial", 11),
                bg="#f8fbff",
                fg="#042c53",
                bd=0,
                highlightbackground="#b5d4f4",
                highlightcolor="#185fa5",
                highlightthickness=1,
                insertbackground="#042c53"
            )
            entry.insert(0, "Masukkan nilai...")
            entry.configure(fg="#8a98a8")
            entry.bind("<FocusIn>", lambda e, ent=entry: self.clear_placeholder(ent))
            entry.bind("<FocusOut>", lambda e, ent=entry: self.restore_placeholder(ent))
            entry.grid(row=1, column=0, sticky="ew", ipady=4)
            self.entries[key] = entry

        separator = tk.Frame(inner_frame, height=1, bg="#e6eef8")
        separator.grid(row=1, column=0, sticky="ew", pady=(10, 10))

        status_section = tk.Frame(inner_frame, bg="#FFFFFF")
        status_section.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        status_title_lbl = tk.Label(
            status_section,
            text="Status Kondisi SSD",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#185fa5",
            anchor="w"
        )
        status_title_lbl.pack(anchor="w", pady=(0, 8))

        cards_container = tk.Frame(status_section, bg="#FFFFFF")
        cards_container.pack(fill="x")
        cards_container.columnconfigure(0, weight=1, uniform="status")
        cards_container.columnconfigure(1, weight=1, uniform="status")

        self.card_normal = tk.Frame(
            cards_container,
            bg="#FFFFFF",
            highlightbackground="#b5d4f4",
            highlightthickness=1,
            bd=0,
            cursor="hand2"
        )
        self.card_normal.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=3)
        self.card_normal.bind("<Button-1>", lambda e: self.select_status("Normal"))

        card_normal_inner = tk.Frame(self.card_normal, bg="#FFFFFF", padx=10, pady=8)
        card_normal_inner.pack(fill="both", expand=True)
        card_normal_inner.bind("<Button-1>", lambda e: self.select_status("Normal"))

        icon_normal_canvas = tk.Canvas(card_normal_inner, width=28, height=28, bg="#FFFFFF", bd=0, highlightthickness=0)
        icon_normal_canvas.grid(row=0, column=0, rowspan=2, padx=(0, 6))
        icon_normal_canvas.create_oval(2, 2, 26, 26, fill="#c0dd97", outline="")
        icon_normal_canvas.create_text(14, 14, text="N", font=("Arial", 10, "bold"), fill="#3b6d11")
        icon_normal_canvas.bind("<Button-1>", lambda e: self.select_status("Normal"))

        lbl_normal_title = tk.Label(
            card_normal_inner,
            text="Normal",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#3b6d11"
        )
        lbl_normal_title.grid(row=0, column=1, sticky="w")
        lbl_normal_title.bind("<Button-1>", lambda e: self.select_status("Normal"))

        lbl_normal_desc = tk.Label(
            card_normal_inner,
            text="SSD berfungsi dengan baik",
            font=("Arial", 8),
            bg="#FFFFFF",
            fg="#888"
        )
        lbl_normal_desc.grid(row=1, column=1, sticky="w")
        lbl_normal_desc.bind("<Button-1>", lambda e: self.select_status("Normal"))

        self.radio_normal_canvas = tk.Canvas(card_normal_inner, width=14, height=14, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.radio_normal_canvas.grid(row=0, column=2, rowspan=2, padx=(6, 0))
        self.radio_normal_canvas.bind("<Button-1>", lambda e: self.select_status("Normal"))

        self.card_rusak = tk.Frame(
            cards_container,
            bg="#FFFFFF",
            highlightbackground="#b5d4f4",
            highlightthickness=1,
            bd=0,
            cursor="hand2"
        )
        self.card_rusak.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=3)
        self.card_rusak.bind("<Button-1>", lambda e: self.select_status("Rusak"))

        card_rusak_inner = tk.Frame(self.card_rusak, bg="#FFFFFF", padx=10, pady=8)
        card_rusak_inner.pack(fill="both", expand=True)
        card_rusak_inner.bind("<Button-1>", lambda e: self.select_status("Rusak"))

        icon_rusak_canvas = tk.Canvas(card_rusak_inner, width=28, height=28, bg="#FFFFFF", bd=0, highlightthickness=0)
        icon_rusak_canvas.grid(row=0, column=0, rowspan=2, padx=(0, 6))
        icon_rusak_canvas.create_oval(2, 2, 26, 26, fill="#f7c1c1", outline="")
        icon_rusak_canvas.create_text(14, 14, text="R", font=("Arial", 10, "bold"), fill="#a32d2d")
        icon_rusak_canvas.bind("<Button-1>", lambda e: self.select_status("Rusak"))

        lbl_rusak_title = tk.Label(
            card_rusak_inner,
            text="Rusak",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#a32d2d"
        )
        lbl_rusak_title.grid(row=0, column=1, sticky="w")
        lbl_rusak_title.bind("<Button-1>", lambda e: self.select_status("Rusak"))

        lbl_rusak_desc = tk.Label(
            card_rusak_inner,
            text="SSD terdeteksi mengalami kerusakan",
            font=("Arial", 8),
            bg="#FFFFFF",
            fg="#888"
        )
        lbl_rusak_desc.grid(row=1, column=1, sticky="w")
        lbl_rusak_desc.bind("<Button-1>", lambda e: self.select_status("Rusak"))

        self.radio_rusak_canvas = tk.Canvas(card_rusak_inner, width=14, height=14, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.radio_rusak_canvas.grid(row=0, column=2, rowspan=2, padx=(6, 0))
        self.radio_rusak_canvas.bind("<Button-1>", lambda e: self.select_status("Rusak"))

        self.update_status_cards()

        btn_container = tk.Frame(inner_frame, bg="#FFFFFF")
        btn_container.grid(row=3, column=0, sticky="ew")

        btn_reset = tk.Button(
            btn_container,
            text="Reset",
            font=("Arial", 9, "bold"),
            bg="#FFFFFF",
            fg="#185fa5",
            bd=0,
            highlightbackground="#b5d4f4",
            highlightthickness=1,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.reset_form
        )
        btn_reset.pack(side="right", padx=(0, 8))

        btn_save = tk.Button(
            btn_container,
            text="Simpan",
            font=("Arial", 9, "bold"),
            bg="#185fa5",
            fg="#FFFFFF",
            bd=0,
            padx=18,
            pady=6,
            cursor="hand2",
            command=self.save_to_dataset
        )
        btn_save.pack(side="right")

        self.btn_train = tk.Button(
            btn_container,
            text="Latih Ulang Model",
            font=("Arial", 9, "bold"),
            bg="#3b6d11",
            fg="#FFFFFF",
            bd=0,
            padx=18,
            pady=6,
            cursor="hand2",
            command=self.start_retrain_thread
        )
        self.btn_train.pack(side="right", padx=(0, 8))

        status_container = tk.Frame(inner_frame, bg="#FFFFFF")
        status_container.grid(row=4, column=0, sticky="ew", pady=(8, 0))

        status_label = tk.Label(
            status_container,
            textvariable=self.train_status_var,
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#185fa5",
            anchor="w"
        )
        status_label.pack(side="left")

        info_wrap = tk.Frame(body, bg="#eef4fb")
        info_wrap.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        info_inner = tk.Frame(info_wrap, bg="#FFFFFF", bd=0)
        info_inner.pack(fill="x", expand=True)

        icon_canvas = tk.Canvas(info_inner, width=20, height=20, bg="#FFFFFF", bd=0, highlightthickness=0)
        icon_canvas.pack(side="left", padx=(22, 10), pady=10)
        icon_canvas.create_oval(1, 1, 19, 19, fill="#185fa5", outline="")
        icon_canvas.create_text(10, 10, text="i", font=("Arial", 12, "bold"), fill="#FFFFFF")

        info_text = tk.Label(
            info_inner,
            text="Data baru akan masuk ke dataset.csv. Pastikan menekan tombol Simpan sebelum Latih Ulang Model.",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#1E3A8A",
            anchor="w"
        )
        info_text.pack(side="left", fill="x", expand=True, pady=10)

        footer_bar = tk.Frame(body, bg="#1e3a5f", height=12)
        footer_bar.grid(row=2, column=0, sticky="ew")
        footer_bar.grid_propagate(False)

    def clear_placeholder(self, entry):
        if entry.get() == "Masukkan nilai...":
            entry.delete(0, tk.END)
            entry.configure(fg="#042c53")

    def restore_placeholder(self, entry):
        if not entry.get().strip():
            entry.insert(0, "Masukkan nilai...")
            entry.configure(fg="#8a98a8")

    def select_status(self, status):
        self.selected_status.set(status)
        self.update_status_cards()

    def update_status_cards(self):
        current = self.selected_status.get()
        
        if current == "Normal":
            self.card_normal.configure(highlightbackground="#3b6d11", bg="#eaf3de")
            self.card_rusak.configure(highlightbackground="#b5d4f4", bg="#FFFFFF")
            
            self.radio_normal_canvas.delete("all")
            self.radio_normal_canvas.create_oval(2, 2, 14, 14, fill="#3b6d11", outline="#3b6d11", width=2)
            self.radio_normal_canvas.create_oval(5, 5, 11, 11, fill="#FFFFFF", outline="")
            
            self.radio_rusak_canvas.delete("all")
            self.radio_rusak_canvas.create_oval(2, 2, 14, 14, fill="#FFFFFF", outline="#b5d4f4", width=2)
        else:
            self.card_normal.configure(highlightbackground="#b5d4f4", bg="#FFFFFF")
            self.card_rusak.configure(highlightbackground="#a32d2d", bg="#fcebeb")
            
            self.radio_normal_canvas.delete("all")
            self.radio_normal_canvas.create_oval(2, 2, 14, 14, fill="#FFFFFF", outline="#b5d4f4", width=2)
            
            self.radio_rusak_canvas.delete("all")
            self.radio_rusak_canvas.create_oval(2, 2, 14, 14, fill="#a32d2d", outline="#a32d2d", width=2)
            self.radio_rusak_canvas.create_oval(5, 5, 11, 11, fill="#FFFFFF", outline="")

    def validate_inputs(self):
        """
        Validasi input numerik non-negatif.
        """
        inputs = {}
        for key in self.param_keys:
            val = self.entries[key].get().strip()
            if not val or val == "Masukkan nilai...":
                messagebox.showerror("Error Validasi", f"Parameter '{self.param_labels[key]}' tidak boleh kosong!")
                return None
            val_clean = val.replace(",", ".")
            try:
                num = float(val_clean)
                if num < 0:
                    messagebox.showerror("Error Validasi", f"Nilai '{self.param_labels[key]}' tidak boleh negatif!")
                    return None
                if key in ["Reallocated_Sector_Count", "Hardware_ECC_Recovered", 
                           "Current_Pending_Sector_Count", "UltraDMA_CRC_Error_Count", 
                           "Power_On_Hours", "Power_Cycle_Count"]:
                    inputs[key] = int(num)
                else:
                    inputs[key] = num
            except ValueError:
                messagebox.showerror("Error Validasi", f"Nilai '{self.param_labels[key]}' harus berupa angka!")
                return None
        return inputs

    def reset_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, "Masukkan nilai...")
            entry.configure(fg="#8a98a8")
        self.selected_status.set("Normal")
        self.update_status_cards()

    def save_to_dataset(self):
        """
        Menyimpan data masukan ke file dataset.csv.
        """
        inputs = self.validate_inputs()
        if inputs is None:
            return

        selected_status = self.selected_status.get()

        if not os.path.exists(DATASET_PATH):
            messagebox.showerror("Error Dataset", f"File dataset tidak ditemukan di:\n{DATASET_PATH}")
            return

        try:
            # Baca dataset.csv dengan separator ';'
            df = pd.read_csv(DATASET_PATH, sep=";")
            next_no = int(df['No'].max()) + 1 if len(df) > 0 else 1

            new_row = {
                "No": next_no,
                "Reallocated_Sector_Count": inputs["Reallocated_Sector_Count"],
                "Hardware_ECC_Recovered": inputs["Hardware_ECC_Recovered"],
                "Current_Pending_Sector_Count": inputs["Current_Pending_Sector_Count"],
                "UltraDMA_CRC_Error_Count": inputs["UltraDMA_CRC_Error_Count"],
                "Power_On_Hours": inputs["Power_On_Hours"],
                "Power_Cycle_Count": inputs["Power_Cycle_Count"],
                "Total_LBA_Written": inputs["Total_LBA_Written"],
                "Total_LBA_Read": inputs["Total_LBA_Read"],
                "Status": selected_status
            }

            # Simpan baris baru ke CSV
            new_df = pd.DataFrame([new_row])
            new_df.to_csv(DATASET_PATH, mode='a', sep=';', header=False, index=False)

            messagebox.showinfo(
                "Sukses",
                f"Data berhasil ditambahkan ke dataset.csv dengan No: {next_no}!\n\n"
                f"Langkah berikutnya: Tekan tombol 'Latih Ulang Model C4.5' untuk melatih kembali pohon keputusan."
            )
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error Menyimpan", f"Gagal menambahkan data ke dataset.csv:\n{str(e)}")

    def start_retrain_thread(self):
        self.train_status_var.set("Melatih ulang model, mohon tunggu...")
        self.btn_train.configure(state="disabled", bg="#8c8c8c")

        thread = threading.Thread(target=self.run_retrain_process)
        thread.daemon = True
        thread.start()

    def run_retrain_process(self):
        """
        Menjalankan script train_model.py.
        """
        python_exec = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
        if not os.path.exists(python_exec):
            python_exec = "python"

        try:
            script_path = os.path.join(BASE_DIR, "train_model.py")
            result = subprocess.run(
                [python_exec, script_path],
                cwd=BASE_DIR,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            if result.returncode == 0:
                self.after(0, self.on_retrain_success)
            else:
                error_msg = result.stderr if result.stderr else "Kesalahan latih tidak diketahui."
                self.after(0, lambda: self.on_retrain_failure(error_msg))
        except Exception as e:
            self.after(0, lambda: self.on_retrain_failure(str(e)))

    def on_retrain_success(self):
        self.train_status_var.set("Model Siap")
        self.btn_train.configure(state="normal", bg="#3b6d11")
        messagebox.showinfo("Sukses", "Model C4.5 berhasil dilatih ulang dengan dataset terbaru!")

    def on_retrain_failure(self, error_message):
        self.train_status_var.set("Gagal melatih model")
        self.btn_train.configure(state="normal", bg="#3b6d11")
        messagebox.showerror("Error Pelatihan", f"Gagal melatih ulang model:\n{error_message}")
        self.train_status_var.set("Model Siap")

    def on_show_page(self):
        """
        Fungsi pemikat saat halaman aktif.
        """
        pass
