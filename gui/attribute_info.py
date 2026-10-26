import tkinter as tk
from tkinter import ttk


def show_attribute_info(parent):
    popup = tk.Toplevel(parent)
    popup.title("Keterangan Parameter SMART SSD")
    popup.geometry("960x580")
    popup.configure(bg="#eef4fb")
    popup.resizable(True, True)

    tk.Frame(popup, bg="#185fa5", height=4).pack(fill="x")
    hdr = tk.Frame(popup, bg="#185fa5", padx=20, pady=14)
    hdr.pack(fill="x")
    tk.Label(hdr,
             text="Daftar Keterangan Parameter S.M.A.R.T SSD",
             font=("Segoe UI", 14, "bold"),
             bg="#185fa5", fg="#FFFFFF").pack(anchor="w")

    tf = tk.Frame(popup, bg="#FFFFFF", padx=16, pady=16)
    tf.pack(fill="both", expand=True)

    canvas = tk.Canvas(tf, bg="#FFFFFF", bd=0, highlightthickness=0)
    v_scroll = ttk.Scrollbar(tf, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=v_scroll.set)

    v_scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    container = tk.Frame(canvas, bg="#FFFFFF")
    canvas.create_window((0, 0), window=container, anchor="nw", tags="root")

    header_frame = tk.Frame(container, bg="#142a52")
    header_frame.pack(fill="x")
    header_frame.columnconfigure(0, minsize=60, weight=0)
    header_frame.columnconfigure(1, minsize=250, weight=0)
    header_frame.columnconfigure(2, weight=1)

    tk.Label(header_frame, text="No", font=("Segoe UI", 12, "bold"),
             bg="#142a52", fg="#FFFFFF", anchor="center",
             padx=6, pady=6).grid(row=0, column=0, sticky="nsew")

    vline1_h = tk.Frame(header_frame, bg="#4a6a9a", width=1)
    vline1_h.grid(row=0, column=0, sticky="nse")

    tk.Label(header_frame, text="Atribut SMART", font=("Segoe UI", 12, "bold"),
             bg="#142a52", fg="#FFFFFF", anchor="center",
             padx=6, pady=8).grid(row=0, column=1, sticky="nsew")

    vline2_h = tk.Frame(header_frame, bg="#4a6a9a", width=1)
    vline2_h.grid(row=0, column=1, sticky="nse")

    tk.Label(header_frame, text="Deskripsi", font=("Segoe UI", 12, "bold"),
             bg="#142a52", fg="#FFFFFF", anchor="center",
             padx=6, pady=8).grid(row=0, column=2, sticky="nsew")

    vline3_h = tk.Frame(header_frame, bg="#4a6a9a", width=1)
    vline3_h.grid(row=0, column=2, sticky="nse")

    hline = tk.Frame(container, bg="#d5dce8", height=1)
    hline.pack(fill="x")

    row_data = [
        ("1", "Reallocated Sector Count",
         "Jumlah sektor buruk (bad sector) yang telah direalokasi ke sektor cadangan. Semakin tinggi nilai atribut ini, semakin banyak sektor yang mengalami realokasi, sehingga mengindikasikan penurunan kondisi SSD dan meningkatnya risiko kegagalan."),
        ("2", "Hardware ECC Recovered",
         "Menunjukkan jumlah kesalahan pembacaan atau penulisan data yang berhasil diperbaiki oleh mekanisme Error Correction Code (ECC). Nilai yang tinggi dapat menunjukkan peningkatan kesalahan media penyimpanan."),
        ("3", "Current Pending Sector Count",
         "Menunjukkan jumlah sektor yang dicurigai mengalami kerusakan dan menunggu proses verifikasi atau realokasi. Nilai yang tinggi mengindikasikan potensi kegagalan SSD."),
        ("4", "UltraDMA CRC Error Count",
         "Menunjukkan jumlah kesalahan komunikasi data antara SSD dan pengontrol (controller) yang disebabkan oleh kesalahan Cyclic Redundancy Check (CRC)."),
        ("5", "Power-On Hours",
         "Menunjukkan total waktu operasional SSD sejak pertama kali digunakan, biasanya dinyatakan dalam satuan jam. Atribut ini digunakan untuk memperkirakan umur pemakaian SSD."),
        ("6", "Power Cycle Count",
         "Menunjukkan jumlah siklus hidup-mati (power on/off) SSD sejak pertama kali digunakan. Nilai ini mencerminkan frekuensi penggunaan perangkat."),
        ("7", "Total LBA Written",
         "Menunjukkan total jumlah Logical Block Address (LBA) yang telah ditulis ke SSD selama masa operasional. Nilai ini digunakan untuk mengukur tingkat penggunaan dan keausan SSD."),
        ("8", "Total LBA Read",
         "Menunjukkan total jumlah Logical Block Address (LBA) yang telah dibaca dari SSD selama masa operasional. Nilai ini menggambarkan intensitas aktivitas pembacaan data pada SSD."),
    ]

    for idx, (no, param, desc) in enumerate(row_data):
        bg = "#F0F7FF" if idx % 2 == 0 else "#FFFFFF"

        row_f = tk.Frame(container, bg=bg)
        row_f.pack(fill="x")
        row_f.columnconfigure(0, minsize=60, weight=0)
        row_f.columnconfigure(1, minsize=250, weight=0)
        row_f.columnconfigure(2, weight=1)

        tk.Label(row_f, text=no, font=("Segoe UI", 10),
                 bg=bg, fg="#1E293B", anchor="center",
                 padx=6, pady=7).grid(row=0, column=0, sticky="nsew")

        tk.Frame(row_f, bg="#d5dce8", width=1).grid(row=0, column=0, sticky="nse")

        tk.Label(row_f, text=param, font=("Segoe UI", 10),
                 bg=bg, fg="#1E293B", anchor="w", justify="left", wraplength=230,
                 padx=6, pady=7).grid(row=0, column=1, sticky="nsew")

        tk.Frame(row_f, bg="#d5dce8", width=1).grid(row=0, column=1, sticky="nse")

        tk.Label(row_f, text=desc, font=("Segoe UI", 10),
                 bg=bg, fg="#1E293B", anchor="w", justify="left", wraplength=540,
                 padx=6, pady=7).grid(row=0, column=2, sticky="nsew")

        tk.Frame(row_f, bg="#d5dce8", width=1).grid(row=0, column=2, sticky="nse")

        tk.Frame(container, bg="#d5dce8", height=1).pack(fill="x")

    def on_canvas_configure(event):
        w = event.width
        if w > 60 + 250 + 50:
            label_w = max(100, w - 60 - 250 - 12)
            for child in container.winfo_children():
                for c in child.winfo_children():
                    if isinstance(c, tk.Label) and c.cget('wraplength') > 100:
                        c.configure(wraplength=label_w)
        canvas.itemconfig("root", width=w)

    canvas.bind("<Configure>", on_canvas_configure)
    container.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    bf = tk.Frame(popup, bg="#eef4fb", pady=12)
    bf.pack(fill="x")
    tk.Button(bf, text="Tutup",
              font=("Segoe UI", 10, "bold"),
              bg="#185fa5", fg="#FFFFFF",
              bd=0, padx=24, pady=7,
              cursor="hand2",
              command=popup.destroy).pack(side="right", padx=16)
