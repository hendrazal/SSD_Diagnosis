import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import math
import joblib
import pandas as pd

from config import MODEL_PATH, BASE_DIR
from gui.attribute_info import show_attribute_info


class VisualizationPage(tk.Frame):
    """
    Halaman Visualisasi C4.5 Dinamis.
    Menampilkan pohon keputusan C4.5 kustom secara visual menggunakan Canvas Tkinter
    dengan highlight jalur keputusan berdasarkan diagnosis terakhir.
    """

    def __init__(self, parent_container, controller):
        super().__init__(parent_container, bg="#eef4fb")
        self.controller = controller

        self.model         = None
        self.decision_path = []

        self._base_zoom   = 0.8
        self.zoom_level   = self._base_zoom
        self._min_zoom    = self._base_zoom
        self._default_zoom = self._base_zoom
        self._initial_zoom_multiplier = 1.0
        self._user_zoomed = False

        # Ukuran canvas — akan diisi setelah widget render
        self.canvas_visible_width  = 0
        self.canvas_visible_height = 0

        self.create_widgets()
        self.on_show_page()

    # ─────────────────────────────────────────────
    # KONSTANTA LAYOUT  (px, sebelum zoom)
    # ─────────────────────────────────────────────
    _NODE_W = 105   # lebar node keputusan
    _NODE_H = 42    # tinggi node keputusan
    _LEAF_W = 85    # lebar node daun
    _LEAF_H = 44    # tinggi node daun
    _H_GAP  = 65    # jarak horizontal minimum antar saudara
    _V_GAP  = 90    # jarak vertikal antar level
    _PAD_X  = 60    # padding kiri-kanan canvas
    _PAD_Y  = 50    # padding atas-bawah canvas

    # ─────────────────────────────────────────────
    # BUILD UI
    # ─────────────────────────────────────────────
    def create_widgets(self):

        # ── Header ───────────────────────────────
        hdr_card = tk.Frame(self, bg="#FFFFFF",
                            highlightbackground="#d5e6fb",
                            highlightthickness=1, bd=0)
        hdr_card.pack(fill="x", pady=(8, 8))

        hdr_inner = tk.Frame(hdr_card, bg="#FFFFFF", padx=22, pady=12)
        hdr_inner.pack(fill="x")

        tb = tk.Frame(hdr_inner, bg="#FFFFFF")
        tb.pack(side="left", fill="x", expand=True)

        tk.Label(tb, text="Visualisasi C4.5",
                 font=("Arial", 16, "bold"),
                 bg="#FFFFFF", fg="#0c447c").pack(anchor="w")
        tk.Label(tb,
                 text="Struktur pohon keputusan kustom dengan highlight jalur diagnosis terakhir.",
                 font=("Arial", 9), bg="#FFFFFF", fg="#3b6f9f").pack(anchor="w", pady=(3, 0))

        tk.Button(hdr_inner, text="Kembali",
                  font=("Arial", 9, "bold"),
                  bg="#FFFFFF", fg="#185fa5", bd=0,
                  highlightbackground="#b5d4f4", highlightthickness=1,
                  padx=14, pady=6, cursor="hand2",
                  command=lambda: self.controller.show_page("ResultPage")
                  ).pack(side="right", padx=(12, 0))

        # ── Body ─────────────────────────────────
        body = tk.Frame(self, bg="#eef4fb")
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)
        body.rowconfigure(1, weight=0)
        body.rowconfigure(2, weight=0)

        card = tk.Frame(body, bg="#FFFFFF",
                        highlightbackground="#b5d4f4",
                        highlightthickness=1, bd=0)
        card.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(2, weight=1)

        tk.Frame(card, bg="#185fa5", height=4).grid(row=0, column=0, sticky="ew")

        # ── Stats cards ───────────────────────────
        top = tk.Frame(card, bg="#FFFFFF", padx=22, pady=10)
        top.grid(row=1, column=0, sticky="ew")
        top.columnconfigure(0, weight=1)

        sf = tk.Frame(top, bg="#FFFFFF")
        sf.pack(fill="x", pady=(0, 6))

        self.cards = {}
        for i, (title, val, color) in enumerate([
            ("Akurasi Model",     "0.0%",     "#3498DB"),
            ("Jumlah Data Latih", "0 sampel", "#E67E22"),
            ("Kedalaman Tree",    "0",        "#9B59B6"),
            ("Jumlah Leaf",       "0",        "#1ABC9C"),
        ]):
            sf.columnconfigure(i, weight=1)
            c = tk.Frame(sf, bg="#FFFFFF", bd=0, relief="flat",
                         highlightthickness=1, highlightbackground="#b5d4f4")
            c.grid(row=0, column=i, sticky="nsew", padx=3, pady=3)
            tk.Frame(c, bg=color, width=3).pack(side="left", fill="y")
            inf = tk.Frame(c, bg="#FFFFFF", padx=10, pady=8)
            inf.pack(side="left", fill="both", expand=True)
            tk.Label(inf, text=title, font=("Arial", 8),
                     bg="#FFFFFF", fg="#185fa5").pack(anchor="w")
            v = tk.Label(inf, text=val, font=("Arial", 11, "bold"),
                         bg="#FFFFFF", fg="#0c447c")
            v.pack(anchor="w", pady=(1, 0))
            self.cards[title] = v

        # ── Toolbar zoom ─────────────────────────
        ctrl = tk.Frame(top, bg="#FFFFFF")
        ctrl.pack(fill="x", pady=(0, 4))

        self.status_var = tk.StringVar(value="Status: Model Siap")
        tk.Label(ctrl, textvariable=self.status_var,
                 font=("Arial", 9, "italic"),
                 bg="#FFFFFF", fg="#185fa5").pack(side="left")

        bb = tk.Frame(ctrl, bg="#FFFFFF")
        bb.pack(side="right")
        for lbl, clr, cmd in [
            ("Zoom In",    "#10B981", self.zoom_in),
            ("Zoom Out",   "#F59E0B", self.zoom_out),
            ("Reset Zoom", "#185fa5", self.reset_zoom),
        ]:
            tk.Button(bb, text=lbl, font=("Arial", 9, "bold"),
                      bg=clr, fg="#FFFFFF", bd=0,
                      padx=10, pady=4, cursor="hand2",
                      command=cmd).pack(side="left", padx=3)

        # ── Canvas area ───────────────────────────
        cw = tk.Frame(card, bg="#FFFFFF",
                      highlightthickness=1,
                      highlightbackground="#b5d4f4")
        cw.grid(row=2, column=0, sticky="nsew", padx=22, pady=(0, 10))

        self.v_sb = ttk.Scrollbar(cw, orient="vertical")
        self.v_sb.pack(side="right", fill="y")
        self.h_sb = ttk.Scrollbar(cw, orient="horizontal")
        self.h_sb.pack(side="bottom", fill="x")

        self.canvas = tk.Canvas(cw, bg="#F8FAFC",
                                bd=0, highlightthickness=0,
                                yscrollcommand=self.v_sb.set,
                                xscrollcommand=self.h_sb.set)
        self.canvas.pack(fill="both", expand=True)
        self.v_sb.config(command=self.canvas.yview)
        self.h_sb.config(command=self.canvas.xview)

        # ← bind Configure hanya untuk update ukuran, TIDAK trigger draw
        self.canvas.bind("<Configure>", self._on_configure)
        self.canvas.bind("<ButtonPress-1>",
                         lambda e: self.canvas.scan_mark(e.x, e.y))
        self.canvas.bind("<B1-Motion>",
                         lambda e: self.canvas.scan_dragto(e.x, e.y, gain=1))
        self.canvas.bind("<MouseWheel>", self._on_scroll)
        self.canvas.bind("<Button-4>",   self._on_scroll)
        self.canvas.bind("<Button-5>",   self._on_scroll)

        # ── Tombol keterangan ─────────────────────
        br = tk.Frame(card, bg="#FFFFFF", padx=22)
        br.grid(row=3, column=0, sticky="ew", pady=(0, 14))
        tk.Button(br, text="Lihat Keterangan Atribut",
                  font=("Arial", 10, "bold"),
                  bg="#185fa5", fg="#FFFFFF",
                  bd=0, padx=18, pady=7, cursor="hand2",
                   command=lambda: show_attribute_info(self)).pack(side="right")

        # ── Info bar ─────────────────────────────
        iw = tk.Frame(body, bg="#eef4fb")
        iw.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        ii = tk.Frame(iw, bg="#FFFFFF")
        ii.pack(fill="x", expand=True)

        ic = tk.Canvas(ii, width=20, height=20,
                       bg="#FFFFFF", bd=0, highlightthickness=0)
        ic.pack(side="left", padx=(22, 10), pady=10)
        ic.create_oval(1, 1, 19, 19, fill="#185fa5", outline="")
        ic.create_text(10, 10, text="i",
                       font=("Arial", 12, "bold"), fill="#FFFFFF")

        tk.Label(ii,
                 text="Visualisasi pohon keputusan C4.5 hasil training dari dataset yang tersedia.",
                 font=("Arial", 10), bg="#FFFFFF", fg="#1E3A8A",
                 anchor="w").pack(side="left", fill="x", expand=True, pady=10)

        # ── Footer ───────────────────────────────
        ft = tk.Frame(body, bg="#1e3a5f", height=12)
        ft.grid(row=2, column=0, sticky="ew")
        ft.grid_propagate(False)

    # ─────────────────────────────────────────────
    # EVENTS
    # ─────────────────────────────────────────────

    def _on_configure(self, event):
        """Simpan ukuran canvas yang terlihat — jangan trigger draw di sini."""
        self.canvas_visible_width  = event.width
        self.canvas_visible_height = event.height
        self.canvas.configure(scrollregion=self.canvas.bbox("all") or (0,0,0,0))

    def _on_scroll(self, event):
        if event.state & 0x4:
            if event.num == 4 or event.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(
                    int(-1 * event.delta / 120), "units")

    # ─────────────────────────────────────────────
    # ZOOM
    # ─────────────────────────────────────────────

    def zoom_in(self):
        self._user_zoomed = True
        self.zoom_level = min(6.0, self.zoom_level * 1.25)
        self.draw_tree()

    def zoom_out(self):
        self._user_zoomed = True
        self.zoom_level = max(self._base_zoom, self.zoom_level * 0.8)
        self.draw_tree()

    def reset_zoom(self):
        self._user_zoomed = True
        self.zoom_level = self._base_zoom
        self.draw_tree()
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0)

    # ─────────────────────────────────────────────
    # DATA
    # ─────────────────────────────────────────────

    def on_show_page(self):
        """Dipanggil saat halaman ini ditampilkan."""
        if hasattr(self, '_draw_timer') and self._draw_timer:
            self.after_cancel(self._draw_timer)
        self._user_zoomed = True
        self._default_zoom = self._base_zoom
        self.zoom_level   = self._base_zoom
        self.load_dashboard_metrics()
        self.load_model()
        self.load_decision_path()
        self._draw_timer = self.after(80, self._initial_draw)

    def _initial_draw(self):
        """Draw pertama kali — canvas sudah punya ukuran nyata di sini."""
        self._user_zoomed = True
        self.zoom_level = self._base_zoom
        self._default_zoom = self._base_zoom
        self.draw_tree()

    def load_dashboard_metrics(self):
        mp  = os.path.join(BASE_DIR, "model", "metrics.json")
        acc = "0.0%"
        smp = "0 sampel"
        depth = "0"
        leaves = "0"
        
        if os.path.exists(mp):
            try:
                with open(mp) as f:
                    m = json.load(f)
                
                # Try test_accuracy first, fallback to accuracy
                test_acc = m.get('test_accuracy', m.get('accuracy', 0))
                acc = f"{test_acc * 100:.1f}%"
                
                # Get tree info
                depth = str(m.get('tree_depth', 0))
                leaves = str(m.get('tree_leaves', 0))
                
                # Get dataset size
                ds  = os.path.join(BASE_DIR, "dataset", "dataset.csv")
                if os.path.exists(ds):
                    with open(ds) as f:
                        smp = f"{len(f.readlines()) - 1} sampel"
            except Exception as e:
                print("metrics error:", e)
        
        # Update cards
        if "Akurasi Model" in self.cards:
            self.cards["Akurasi Model"].configure(text=acc)
        if "Jumlah Data Latih" in self.cards:
            self.cards["Jumlah Data Latih"].configure(text=smp)
        if "Kedalaman Tree" in self.cards:
            self.cards["Kedalaman Tree"].configure(text=depth)
        if "Jumlah Leaf" in self.cards:
            self.cards["Jumlah Leaf"].configure(text=leaves)

    def load_model(self):
        self.model = None
        if not os.path.exists(MODEL_PATH):
            messagebox.showwarning("Model Tidak Ditemukan",
                                   "Model C4.5 belum dilatih.")
            return
        try:
            self.model = joblib.load(MODEL_PATH)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat model:\n{e}")

    def load_decision_path(self):
        pred = self.controller.get_shared_data("last_prediction")
        if pred is None or self.model is None:
            self.decision_path = []
            self.status_var.set("Status: Tidak ada data prediksi")
            return
        try:
            node_objects = self.model.get_decision_path(
                pd.Series(pred["inputs"]))
            self.decision_path = node_objects
            self.status_var.set(
                f"Status: Jalur keputusan ({len(node_objects)} node)")
        except Exception as e:
            self.decision_path = []
            self.status_var.set(f"Status: Gagal muat jalur - {e}")

    # ─────────────────────────────────────────────
    # LAYOUT ENGINE  — subtree-width algorithm
    # ─────────────────────────────────────────────

    def _is_leaf(self, node):
        return node is not None and node.label is not None

    def _node_text_lines(self, node):
        if self._is_leaf(node):
            return [node.label, f"Samples: {node.samples}", f"{node.probability*100:.2f}%"]
        attr = node.attribute.replace("_", " ")
        return [attr, f"≤ {math.ceil(node.threshold)}?"]

    def _node_size(self, node):
        lines = self._node_text_lines(node)
        max_chars = max(len(line) for line in lines)
        width = max(70, min(145, max_chars * 6 + 22))
        height = max(32, len(lines) * 13 + 14)
        return width, height

    def _nw(self, node):
        return self._node_size(node)[0]

    def _nh(self, node):
        return self._node_size(node)[1]

    def _subtree_width(self, node):
        """Lebar minimum subtree (px, sebelum zoom)."""
        if node is None:
            return 0
        own = self._nw(node)
        if self._is_leaf(node):
            return own
        lw  = self._subtree_width(node.left)
        rw  = self._subtree_width(node.right)
        gap = self._H_GAP if (lw > 0 and rw > 0) else 0
        return max(own, lw + gap + rw)

    def _assign_positions(self, node, left_edge, depth, pos):
        """
        Hitung posisi CENTER (cx, cy) tiap node.
        left_edge = batas kiri wilayah yang dialokasikan untuk subtree ini.
        """
        if node is None:
            return 0.0

        nw  = self._nw(node)
        nh  = self._nh(node)
        cy  = self._PAD_Y + depth * (self._NODE_H + self._V_GAP)

        if self._is_leaf(node):
            cx = left_edge + nw / 2
            pos[node] = (cx, cy)
            return cx

        lw  = self._subtree_width(node.left)
        rw  = self._subtree_width(node.right)
        gap = self._H_GAP if (lw > 0 and rw > 0) else 0
        total = lw + gap + rw

        # Pastikan wilayah tidak lebih kecil dari lebar node itu sendiri
        if total < nw:
            pad   = (nw - total) / 2
            lw   += pad
            rw   += pad
            total = nw

        self._assign_positions(node.left,  left_edge,           depth + 1, pos)
        self._assign_positions(node.right, left_edge + lw + gap, depth + 1, pos)

        lc = pos[node.left][0]  if node.left  else left_edge + lw / 2
        rc = pos[node.right][0] if node.right else left_edge + lw + gap + rw / 2
        cx = (lc + rc) / 2
        pos[node] = (cx, cy)
        return cx

    # ─────────────────────────────────────────────
    # DRAW
    # ─────────────────────────────────────────────

    def draw_tree(self):
        self.canvas.delete("all")

        if (self.model is None
                or not hasattr(self.model, "root")
                or self.model.root is None):
            self.canvas.create_text(
                max(self.canvas_visible_width  // 2, 300),
                max(self.canvas_visible_height // 2, 150),
                text="Model belum dilatih.\nSilakan latih model terlebih dahulu.",
                font=("Arial", 12, "italic"),
                fill="#7F8C8D", anchor="center"
            )
            return

        # 1. Hitung posisi (koordinat asli, belum zoom)
        pos = {}
        self._assign_positions(self.model.root, self._PAD_X, 0, pos)

        # Normalisasi bounding box pohon agar tidak condong ke kiri/kanan
        min_x = min(cx - self._nw(n) / 2 for n, (cx, _) in pos.items())
        max_x = max(cx + self._nw(n) / 2 for n, (cx, _) in pos.items())
        min_y = min(cy - self._nh(n) / 2 for n, (_, cy) in pos.items())
        max_y = max(cy + self._nh(n) / 2 for n, (_, cy) in pos.items())

        shift_x = self._PAD_X - min_x
        shift_y = self._PAD_Y - min_y
        for n in pos:
            pos[n] = (pos[n][0] + shift_x, pos[n][1] + shift_y)

        tree_w = max_x - min_x
        tree_h = max_y - min_y
        raw_w = tree_w + (self._PAD_X * 2)
        raw_h = tree_h + (self._PAD_Y * 2)

        # 2. Auto-fit — hanya ketika canvas sudah punya ukuran nyata
        cw = self.canvas_visible_width
        ch = self.canvas_visible_height
        if not self._user_zoomed and cw > 50 and ch > 50:
            zx = (cw - 20) / raw_w
            zy = (ch - 20) / raw_h
            self.zoom_level = max(0.15, min(zx, zy, 1.4)) * self._initial_zoom_multiplier
            self._min_zoom = self.zoom_level
            if self._default_zoom is None:
                self._default_zoom = self.zoom_level

        z  = self.zoom_level
        cw_out = int(raw_w * z)
        ch_out = int(raw_h * z)

        display_w = max(cw_out, cw)
        display_h = max(ch_out, ch)
        center_x = max(0, (display_w - cw_out) / 2)
        center_y = max(0, (display_h - ch_out) / 2)

        # Helper scale + center offset
        def sx(v): return (v * z) + center_x
        def sy(v): return (v * z) + center_y

        dec_set = set(self.decision_path)
        path_leaf = self.decision_path[-1] if self.decision_path else None
        path_is_normal = getattr(path_leaf, "label", None) == "Normal"
        path_fill = "#10B981" if path_is_normal else "#DC2626"
        path_out = "#059669" if path_is_normal else "#991B1B"

        # 3. Gambar edges
        def draw_edges(node):
            if node is None or self._is_leaf(node):
                return
            cx, cy  = pos[node]
            nh      = self._nh(node)
            px, py  = sx(cx), sy(cy)
            bot_y   = sy(cy + nh / 2)
            in_path = node in dec_set

            for child, lbl in [
                (node.left,  f"≤ {math.ceil(node.threshold)}"),
                (node.right, f"> {math.ceil(node.threshold)}"),
            ]:
                if child is None:
                    continue
                ccx, ccy = pos[child]
                cnh      = self._nh(child)
                chx      = sx(ccx)
                chy      = sy(ccy - cnh / 2)

                hi    = in_path and child in dec_set
                lc    = path_fill if hi else "#CBD5E1"
                lw    = max(2, int(3 * z)) if hi else max(1, int(1.5 * z))

                # Step-bezier: parent-bottom → elbow → child-top
                mid_y = (bot_y + chy) / 2
                self.canvas.create_line(
                    px,   bot_y,
                    px,   mid_y,
                    chx,  mid_y,
                    chx,  chy,
                    fill=lc, width=lw, smooth=True, tags="edge"
                )

                # Label edge
                fsz = max(6, int(7 * z))
                tf  = ("Arial", fsz, "bold") if hi else ("Arial", fsz)
                tc  = path_fill if hi else "#64748B"
                mx  = (px + chx) / 2
                my  = mid_y

                tid = self.canvas.create_text(
                    mx, my, text=lbl,
                    font=tf, fill=tc, tags="edge_lbl"
                )
                bb = self.canvas.bbox(tid)
                if bb:
                    self.canvas.create_rectangle(
                        bb[0] - 4, bb[1] - 2, bb[2] + 4, bb[3] + 2,
                        fill="#FFFFFF", outline="", tags="edge_bg"
                    )
                    self.canvas.tag_raise(tid)

                draw_edges(child)

        draw_edges(self.model.root)

        # 4. Gambar nodes
        def draw_node(node):
            if node is None:
                return
            cx, cy  = pos[node]
            nw, nh  = self._nw(node), self._nh(node)
            x, y    = sx(cx), sy(cy)
            w2, h2  = (nw * z) / 2, (nh * z) / 2
            in_path = node in dec_set
            is_leaf = self._is_leaf(node)

            x0, y0 = x - w2, y - h2
            x1, y1 = x + w2, y + h2

            # Warna node
            fill, out, tc = "#F0F7FF", "#b5d4f4", "#0c447c"
            if in_path:
                fill, out, tc = path_fill, path_out, "#FFFFFF"
            border = max(1, int(2 * z))

            # Shadow
            self.canvas.create_rectangle(
                x0 + 3, y0 + 3, x1 + 3, y1 + 3,
                fill="#CBD5E1", outline="", tags="shadow"
            )
            # Kotak node
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=fill, outline=out, width=border, tags="node"
            )

            # Teks — wraplength diset ketat agar tidak meluber keluar kotak
            fsz      = max(5, int(6 * z))
            wrap_px  = max(1, int(nw * z) - 16)   # margin 8px kiri+kanan

            txt = "\n".join(self._node_text_lines(node))

            self.canvas.create_text(
                x, y,
                text=txt,
                font=("Arial", fsz, "bold"),
                fill=tc,
                justify="center",
                width=wrap_px,       # ← hard wraplength
                tags="node_txt"
            )

            draw_node(node.left)
            draw_node(node.right)

        draw_node(self.model.root)

        # 5. Update scrollregion
        self.canvas.config(scrollregion=(0, 0, display_w, display_h))
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0)

