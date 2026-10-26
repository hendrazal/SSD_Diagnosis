import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from config import DATASET_PATH
from predict import predict_ssd

class InputPage(tk.Frame):

    def __init__(self, parent_container, controller):
        super().__init__(parent_container, bg="#eef4fb")
        self.controller = controller

        self.param_labels = {
            "Reallocated_Sector_Count": "Reallocated Sectors Count",
            "Hardware_ECC_Recovered": "Hardware ECC Recovered",
            "Current_Pending_Sector_Count": "Current Pending Sector Count",
            "UltraDMA_CRC_Error_Count": "UltraDMA CRC Error Count",
            "Power_On_Hours": "Power-On Hours",
            "Power_Cycle_Count": "Power Cycle Count",
            "Total_LBA_Written": "Total LBAs Written",
            "Total_LBA_Read": "Total LBAs Read"
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
        self.create_widgets()

    def create_widgets(self):
        header_card = tk.Frame(self, bg="#FFFFFF", highlightbackground="#d5e6fb", highlightthickness=1, bd=0)
        header_card.pack(fill="x", pady=(10, 12))

        header_inner = tk.Frame(header_card, bg="#FFFFFF", padx=22, pady=14)
        header_inner.pack(fill="x")

        title_block = tk.Frame(header_inner, bg="#FFFFFF")
        title_block.pack(side="left", fill="x", expand=True)

        title_lbl = tk.Label(
            title_block,
            text="Input Data S.M.A.R.T",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF",
            fg="#0c447c"
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            title_block,
            text="Masukkan nilai atribut SMART SSD untuk memulai proses prediksi kerusakan.",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#3b6f9f"
        )
        subtitle_lbl.pack(anchor="w", pady=(4, 0))

        btn_add_dataset = tk.Button(
            header_inner,
            text="Tambah Dataset",
            font=("Arial", 9, "bold"),
            bg="#185fa5",
            fg="#FFFFFF",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=lambda: self.controller.show_page("DatasetPage")
        )
        btn_add_dataset.pack(side="right", padx=(14, 0))

        body = tk.Frame(self, bg="#eef4fb")
        body.pack(fill="both", expand=True)

        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)
        body.rowconfigure(1, weight=0)
        body.rowconfigure(2, weight=0)

        card_frame = tk.Frame(body, bg="#FFFFFF", highlightbackground="#b5d4f4", highlightthickness=1, bd=0)
        card_frame.grid(row=0, column=0, sticky="new", pady=(0, 6))
        card_frame.columnconfigure(0, weight=1)
        card_frame.rowconfigure(1, weight=1)

        accent = tk.Frame(card_frame, bg="#185fa5", height=4)
        accent.grid(row=0, column=0, sticky="ew")

        inner_frame = tk.Frame(card_frame, bg="#FFFFFF", padx=22, pady=16)
        inner_frame.grid(row=1, column=0, sticky="nsew")
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.rowconfigure(0, weight=1)

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
            field_frame.grid(row=row, column=col, sticky="ew", pady=12)
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
            entry.grid(row=1, column=0, sticky="ew", ipady=6)
            self.entries[key] = entry

        separator = tk.Frame(inner_frame, height=1, bg="#e6eef8")
        separator.grid(row=1, column=0, sticky="ew", pady=(20, 18))

        btn_container = tk.Frame(inner_frame, bg="#FFFFFF")
        btn_container.grid(row=2, column=0, sticky="ew")

        btn_predict = tk.Button(
            btn_container,
            text="Cek Kerusakan",
            font=("Arial", 10, "bold"),
            bg="#185fa5",
            fg="#FFFFFF",
            bd=0,
            padx=24,
            pady=8,
            cursor="hand2",
            command=self.diagnose_ssd
        )
        btn_predict.pack(side="right")

        btn_reset = tk.Button(
            btn_container,
            text="Reset",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#185fa5",
            bd=0,
            highlightbackground="#b5d4f4",
            highlightthickness=1,
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.reset_form
        )
        btn_reset.pack(side="right", padx=(0, 10))

        info_wrap = tk.Frame(body, bg="#eef4fb")
        info_wrap.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        info_inner = tk.Frame(info_wrap, bg="#FFFFFF", bd=0)
        info_inner.pack(fill="x", expand=True, padx=0)

        icon_canvas = tk.Canvas(info_inner, width=20, height=20, bg="#FFFFFF", bd=0, highlightthickness=0)
        icon_canvas.pack(side="left", padx=(22, 10), pady=12)
        icon_canvas.create_oval(1, 1, 19, 19, fill="#185fa5", outline="")
        icon_canvas.create_text(10, 10, text="i", font=("Arial", 12, "bold"), fill="#FFFFFF")

        info_text = tk.Label(
            info_inner,
            text="Pastikan seluruh atribut SMART diisi sebelum melakukan pengecekan kerusakan.",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#1E3A8A",
            anchor="w"
        )
        info_text.pack(side="left", fill="x", expand=True, pady=12)

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

    def validate_inputs(self):
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

    def diagnose_ssd(self):
        inputs = self.validate_inputs()
        if inputs is None:
            return

        try:
            result = predict_ssd(inputs)
            self.controller.set_shared_data("last_prediction", {
                "inputs": inputs,
                "result": result
            })
            self.controller.show_page("ResultPage")
        except Exception as e:
            messagebox.showerror("Error Prediksi", f"Terjadi kesalahan saat mendiagnosis:\n{str(e)}")

    def on_show_page(self):
        pass
