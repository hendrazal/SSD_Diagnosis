import tkinter as tk
from tkinter import ttk

class ScrollableFrame(tk.Frame):
    """
    Frame wrapper with vertical scrollbar.
    Semua child widget di-pack ke dalam `self.scroll`.
    """

    def __init__(self, parent, bg="#F5F6FA", width=None, height=None, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, bg=bg, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll = tk.Frame(self.canvas, bg=bg)
        self.scroll_window = self.canvas.create_window((0, 0), window=self.scroll, anchor="nw")

        self.scroll.bind("<Configure>", self._on_scroll_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.bind_mousewheel()

    def _on_scroll_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.scroll_window, width=event.width)

    def bind_mousewheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
