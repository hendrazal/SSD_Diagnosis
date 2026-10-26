import tkinter as tk
from tkinter import ttk
import numpy as np

from gui.scrollable_frame import ScrollableFrame

class ResultPage(tk.Frame):

    def __init__(self, parent_container, controller):
        super().__init__(parent_container, bg="#eef4fb")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        header_card = tk.Frame(self, bg="#FFFFFF", highlightbackground="#d5e6fb", highlightthickness=1, bd=0)
        header_card.pack(fill="x", pady=(8, 8))

        header_inner = tk.Frame(header_card, bg="#FFFFFF", padx=22, pady=12)
        header_inner.pack(fill="x")

        title_block = tk.Frame(header_inner, bg="#FFFFFF")
        title_block.pack(side="left", fill="x", expand=True)

        header_label = tk.Label(
            title_block,
            text="Hasil Prediksi",
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            fg="#0c447c"
        )
        header_label.pack(anchor="w")

        subtitle_lbl = tk.Label(
            title_block,
            text="Hasil diagnosis status kesehatan SSD berdasarkan data SMART yang diinput.",
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

        self.card_frame = tk.Frame(body, bg="#FFFFFF", highlightbackground="#b5d4f4", highlightthickness=1, bd=0)
        self.card_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        self.card_frame.columnconfigure(0, weight=1)
        self.card_frame.rowconfigure(1, weight=1)
        self.card_frame.rowconfigure(2, weight=0)

        accent = tk.Frame(self.card_frame, bg="#185fa5", height=4)
        accent.grid(row=0, column=0, sticky="ew")

        self.scroll_container = ScrollableFrame(self.card_frame, bg="#FFFFFF")
        self.scroll_container.grid(row=1, column=0, sticky="nsew")

        self.scroll_inner = tk.Frame(self.scroll_container.scroll, bg="#FFFFFF", padx=22, pady=10)
        self.scroll_inner.pack(fill="x")

        self.btn_frame = tk.Frame(self.card_frame, bg="#FFFFFF", padx=22)
        self.btn_frame.grid(row=2, column=0, sticky="ew", pady=(14, 18))

        self.btn_visualize = tk.Button(
            self.btn_frame,
            text="Lihat Visualisasi",
            font=("Arial", 10, "bold"),
            bg="#534ab7",
            fg="#FFFFFF",
            bd=0,
            padx=22,
            pady=8,
            cursor="hand2",
            command=lambda: self.controller.show_page("VisualizationPage")
        )
        self.btn_visualize.pack(side="right")

        self.show_no_data()

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
            text="Hasil prediksi berdasarkan model C4.5 yang telah dilatih dengan dataset tersedia.",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#1E3A8A",
            anchor="w"
        )
        info_text.pack(side="left", fill="x", expand=True, pady=10)

        footer_bar = tk.Frame(body, bg="#1e3a5f", height=12)
        footer_bar.grid(row=2, column=0, sticky="ew")
        footer_bar.grid_propagate(False)

    def show_no_data(self):
        for widget in self.scroll_inner.winfo_children():
            widget.destroy()

        no_data_label = tk.Label(
            self.scroll_inner,
            text="Belum ada data diagnosis.\nSilakan masukkan nilai SMART SSD terlebih dahulu.",
            font=("Arial", 12, "italic"),
            bg="#FFFFFF",
            fg="#7F8C8D",
            pady=60
        )
        no_data_label.pack(fill="both", expand=True)

    def on_show_page(self):
        pred_data = self.controller.get_shared_data("last_prediction")
        if pred_data is None:
            self.show_no_data()
        else:
            self.update_result_ui(pred_data["inputs"], pred_data["result"])

    def update_result_ui(self, inputs, result):
        for widget in self.scroll_inner.winfo_children():
            widget.destroy()

        status = result["status"]
        confidence = result["confidence"]

        is_normal = status == "Normal"

        if is_normal:
            bg_outer = "#c0dd97"
            bg_inner = "#eaf3de"
            border_color = "#97c459"
            status_text = "SSD Normal"
            icon_symbol = "\u2713"
            icon_color = "#3b6d11"
            status_color = "#27500a"
            desc_color = "#3b6d11"
            desc_text = "SSD Anda dalam kondisi baik dan tidak terdeteksi adanya kerusakan. Pemantauan rutin tetap disarankan untuk menjaga performa optimal."
        else:
            bg_outer = "#f7c1c1"
            bg_inner = "#fcebeb"
            border_color = "#e24b4a"
            status_text = "SSD Rusak"
            icon_symbol = "\u26a0"
            icon_color = "#a32d2d"
            status_color = "#791f1f"
            desc_color = "#a32d2d"
            desc_text = "SSD Anda terindikasi mengalami kerusakan atau anomali. Sangat disarankan untuk segera melakukan backup data penting."

        self.scroll_inner.columnconfigure(0, weight=1)

        row = 0
        status_outer = tk.Frame(self.scroll_inner, bg=bg_outer, highlightbackground=border_color, highlightthickness=2, bd=0)
        status_outer.grid(row=row, column=0, sticky="ew", pady=(0, 10))

        status_inner = tk.Frame(status_outer, bg=bg_inner, bd=0)
        status_inner.pack(fill="x", padx=2, pady=2)

        status_content = tk.Frame(status_inner, bg=bg_inner)
        status_content.pack(padx=20, pady=10)

        icon_canvas = tk.Canvas(status_content, width=46, height=46, bg=bg_inner, bd=0, highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_oval(2, 2, 44, 44, fill="#FFFFFF", outline="")
        icon_canvas.create_text(23, 23, text=icon_symbol, font=("Arial", 20, "bold"), fill=icon_color)

        status_lbl = tk.Label(
            status_content,
            text=status_text,
            font=("Arial", 16, "bold"),
            bg=bg_inner,
            fg=status_color
        )
        status_lbl.pack(pady=(4, 2))

        desc_lbl = tk.Label(
            status_content,
            text=desc_text,
            font=("Arial", 9),
            bg=bg_inner,
            fg=desc_color,
            wraplength=500,
            justify="center"
        )
        desc_lbl.pack()

        row += 1
        prob_label = tk.Label(
            self.scroll_inner,
            text="Probabilitas Prediksi",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#185fa5",
            anchor="w"
        )
        prob_label.grid(row=row, column=0, sticky="w", pady=(0, 6))

        row += 1
        prob_grid = tk.Frame(self.scroll_inner, bg="#FFFFFF")
        prob_grid.grid(row=row, column=0, sticky="ew")
        prob_grid.columnconfigure(0, weight=1, uniform="prob")
        prob_grid.columnconfigure(1, weight=1, uniform="prob")

        prob_normal = confidence if is_normal else (100.0 - confidence)
        prob_rusak = confidence if not is_normal else (100.0 - confidence)

        prob_card_normal = tk.Frame(prob_grid, bg="#FFFFFF", highlightbackground="#b5d4f4", highlightthickness=1, bd=0)
        prob_card_normal.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        prob_card_normal_inner = tk.Frame(prob_card_normal, bg="#FFFFFF", padx=10, pady=8)
        prob_card_normal_inner.pack(fill="x")

        header_n = tk.Frame(prob_card_normal_inner, bg="#FFFFFF")
        header_n.pack(fill="x", pady=(0, 8))

        icon_n = tk.Canvas(header_n, width=14, height=14, bg="#FFFFFF", bd=0, highlightthickness=0)
        icon_n.pack(side="left", padx=(0, 5))
        icon_n.create_oval(0, 0, 14, 14, fill="#c0dd97", outline="")
        icon_n.create_text(7, 7, text="N", font=("Arial", 7, "bold"), fill="#3b6d11")

        lbl_n = tk.Label(header_n, text="Normal", font=("Arial", 10, "bold"), bg="#FFFFFF", fg="#3b6d11")
        lbl_n.pack(side="left")

        val_n = tk.Label(header_n, text=f"{prob_normal:.0f}%", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#27500a")
        val_n.pack(side="right")

        self._create_rounded_bar(prob_card_normal_inner, prob_normal, "#639922")

        prob_card_rusak = tk.Frame(prob_grid, bg="#FFFFFF", highlightbackground="#b5d4f4", highlightthickness=1, bd=0)
        prob_card_rusak.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        prob_card_rusak_inner = tk.Frame(prob_card_rusak, bg="#FFFFFF", padx=10, pady=8)
        prob_card_rusak_inner.pack(fill="x")

        header_r = tk.Frame(prob_card_rusak_inner, bg="#FFFFFF")
        header_r.pack(fill="x", pady=(0, 8))

        icon_r = tk.Canvas(header_r, width=14, height=14, bg="#FFFFFF", bd=0, highlightthickness=0)
        icon_r.pack(side="left", padx=(0, 5))
        icon_r.create_oval(0, 0, 14, 14, fill="#f7c1c1", outline="")
        icon_r.create_text(7, 7, text="R", font=("Arial", 7, "bold"), fill="#a32d2d")

        lbl_r = tk.Label(header_r, text="Rusak", font=("Arial", 10, "bold"), bg="#FFFFFF", fg="#a32d2d")
        lbl_r.pack(side="left")

        val_r = tk.Label(header_r, text=f"{prob_rusak:.0f}%", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#791f1f")
        val_r.pack(side="right")

        self._create_rounded_bar(prob_card_rusak_inner, prob_rusak, "#a32d2d")

        row += 1
        smart_label = tk.Label(
            self.scroll_inner,
            text="Ringkasan Data SMART Yang Diinput",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#185fa5",
            anchor="w"
        )
        smart_label.grid(row=row, column=0, sticky="w", pady=(6, 6))

        row += 1
        smart_grid = tk.Frame(self.scroll_inner, bg="#FFFFFF", highlightbackground="#b5d4f4", highlightthickness=1, bd=0)
        smart_grid.grid(row=row, column=0, sticky="ew", pady=(0, 14))

        all_params = [
            ("Reallocated_Sector_Count", "Reallocated SC"),
            ("Hardware_ECC_Recovered", "HW ECC Recovered"),
            ("Current_Pending_Sector_Count", "Pending SC"),
            ("UltraDMA_CRC_Error_Count", "UltraDMA CRC"),
            ("Power_On_Hours", "Power On Hours"),
            ("Power_Cycle_Count", "Power Cycle"),
            ("Total_LBA_Written", "LBA Written"),
            ("Total_LBA_Read", "LBA Read")
        ]

        for i in range(4):
            smart_grid.columnconfigure(i, weight=1, uniform="sm")

        for idx, (key, display_name) in enumerate(all_params):
            val = inputs[key]
            cell = tk.Frame(smart_grid, bg="#FFFFFF", highlightbackground="#b5d4f4", highlightthickness=1)
            cell.grid(row=idx//4, column=idx%4, sticky="nsew")

            cell_inner = tk.Frame(cell, bg="#FFFFFF", padx=6, pady=4)
            cell_inner.pack(fill="both", expand=True)

            lbl_name = tk.Label(cell_inner, text=display_name, font=("Arial", 8, "bold"), bg="#FFFFFF", fg="#185fa5", anchor="w")
            lbl_name.pack(anchor="w", pady=(0, 1))

            if isinstance(val, float):
                val_text = f"{val:,.2f}"
            else:
                val_text = f"{val:,}"

            lbl_val = tk.Label(cell_inner, text=val_text, font=("Courier New", 10, "bold"), bg="#FFFFFF", fg="#042c53", anchor="w")
            lbl_val.pack(anchor="w")

        row += 1
        self.scroll_inner.rowconfigure(row, weight=1)
        spacer = tk.Frame(self.scroll_inner, bg="#FFFFFF")
        spacer.grid(row=row, column=0, sticky="nsew")

    def _create_rounded_bar(self, parent, pct, color):
        c = tk.Canvas(parent, height=14, bg="#FFFFFF", bd=0, highlightthickness=0)
        c.pack(fill="x")

        def draw(event):
            w = event.width
            if w < 10:
                return
            c.delete("all")
            r = 7
            fw = int(w * min(pct, 100) / 100)
            c.create_arc(0, 0, r*2, 14, start=90, extent=180, fill="#e0e0e0", outline="")
            c.create_arc(w-r*2, 0, w, 14, start=-90, extent=180, fill="#e0e0e0", outline="")
            c.create_rectangle(r, 0, w-r, 14, fill="#e0e0e0", outline="")
            if fw > 0:
                if fw >= r*2:
                    c.create_arc(0, 0, r*2, 14, start=90, extent=180, fill=color, outline="")
                    c.create_arc(fw-r*2, 0, fw, 14, start=-90, extent=180, fill=color, outline="")
                    c.create_rectangle(r, 0, fw-r, 14, fill=color, outline="")
                else:
                    c.create_arc(0, 0, fw, 14, start=90, extent=180, fill=color, outline="")

        c.bind("<Configure>", draw)
        return c
