"""
Unit Converter — A clean, beginner-friendly GUI app using Tkinter.
Supports Temperature, Length, and Weight conversions.
Features: Dark/Light theme, conversion history, real-time unit swapping, error handling.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime


# ─────────────────────────────────────────────
#  CONVERSION LOGIC
# ─────────────────────────────────────────────

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        raise ValueError(f"Unknown unit: {from_unit}")

    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    else:
        raise ValueError(f"Unknown unit: {to_unit}")


LENGTH_TO_METER = {
    "Meter": 1.0, "Kilometer": 1000.0, "Centimeter": 0.01,
    "Millimeter": 0.001, "Mile": 1609.344, "Inch": 0.0254, "Foot": 0.3048,
}

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert length using Meter as base unit."""
    return value * LENGTH_TO_METER[from_unit] / LENGTH_TO_METER[to_unit]


WEIGHT_TO_KG = {
    "Kilogram": 1.0, "Gram": 0.001, "Pound": 0.453592, "Ounce": 0.0283495,
}

def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """Convert weight using Kilogram as base unit."""
    return value * WEIGHT_TO_KG[from_unit] / WEIGHT_TO_KG[to_unit]


CATEGORIES = {
    "Temperature": {
        "icon": "🌡",
        "units": ["Celsius", "Fahrenheit", "Kelvin"],
        "converter": convert_temperature,
        "symbols": {"Celsius": "°C", "Fahrenheit": "°F", "Kelvin": "K"},
    },
    "Length": {
        "icon": "📏",
        "units": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Inch", "Foot"],
        "converter": convert_length,
        "symbols": {
            "Meter": "m", "Kilometer": "km", "Centimeter": "cm",
            "Millimeter": "mm", "Mile": "mi", "Inch": "in", "Foot": "ft",
        },
    },
    "Weight": {
        "icon": "⚖",
        "units": ["Kilogram", "Gram", "Pound", "Ounce"],
        "converter": convert_weight,
        "symbols": {"Kilogram": "kg", "Gram": "g", "Pound": "lb", "Ounce": "oz"},
    },
}


# ─────────────────────────────────────────────
#  THEMES
# ─────────────────────────────────────────────

THEMES = {
    "dark": {
        "bg": "#0f0f0f", "panel": "#1a1a1a", "card": "#222222",
        "border": "#333333", "accent": "#f59e0b", "accent_dim": "#b45309",
        "text": "#f5f5f5", "text_dim": "#999999", "text_muted": "#444444",
        "input_bg": "#2a2a2a", "success": "#22c55e", "error": "#ef4444", "hover": "#2e2e2e",
    },
    "light": {
        "bg": "#f5f0e8", "panel": "#ebe4d6", "card": "#ffffff",
        "border": "#d4c9b0", "accent": "#c2410c", "accent_dim": "#9a3412",
        "text": "#1c1917", "text_dim": "#57534e", "text_muted": "#a8a29e",
        "input_bg": "#faf7f2", "success": "#15803d", "error": "#dc2626", "hover": "#f0e8d8",
    },
}


# ─────────────────────────────────────────────
#  APPLICATION
# ─────────────────────────────────────────────

class UnitConverterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("660x800")
        self.root.minsize(560, 660)
        self.root.resizable(True, True)

        self.theme_name = "dark"
        self.history: list[str] = []
        self.selected_cat = "Temperature"

        self._setup_fonts()
        self._build_ui()
        self._apply_theme()
        self._on_category_change()

    def _t(self):
        return THEMES[self.theme_name]

    def _setup_fonts(self):
        self.font_title  = ("Courier New", 18, "bold")
        self.font_label  = ("Courier New", 9, "bold")
        self.font_input  = ("Courier New", 24, "bold")
        self.font_result = ("Courier New", 17, "bold")
        self.font_small  = ("Courier New", 9)
        self.font_btn    = ("Courier New", 10, "bold")
        self.font_hist   = ("Courier New", 9)

    def _build_ui(self):
        t = self._t()

        # Canvas + scrollbar for scrollable content
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bd=0)
        self.vbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbar.set)
        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.main = tk.Frame(self.canvas)
        self._cwin = self.canvas.create_window((0, 0), window=self.main, anchor="nw")
        self.main.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self._cwin, width=e.width))
        self.root.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.root.bind_all("<Button-4>",   lambda e: self.canvas.yview_scroll(-1, "units"))
        self.root.bind_all("<Button-5>",   lambda e: self.canvas.yview_scroll(1, "units"))

        P = {"padx": 20, "pady": 6}

        # ── Header ──────────────────────────────
        self.frm_header = tk.Frame(self.main)
        self.frm_header.pack(fill="x", padx=0, pady=0)

        self.lbl_title = tk.Label(self.frm_header, text="◈ UNIT CONVERTER", font=self.font_title)
        self.lbl_title.pack(side="left", padx=24, pady=14)

        self.btn_theme = tk.Button(
            self.frm_header, text="☀ LIGHT", font=("Courier New", 8, "bold"),
            relief="flat", cursor="hand2", bd=0, padx=10, pady=5,
            command=self._toggle_theme
        )
        self.btn_theme.pack(side="right", padx=16, pady=14)

        self.frm_sep = tk.Frame(self.main, height=1)
        self.frm_sep.pack(fill="x")

        # ── Category Tabs ───────────────────────
        self.frm_cat = tk.LabelFrame(self.main, text=" CATEGORY ", font=self.font_label, bd=1, relief="flat")
        self.frm_cat.pack(fill="x", **P)

        self.cat_row = tk.Frame(self.frm_cat)
        self.cat_row.pack(fill="x", padx=8, pady=10)

        self.cat_btns: dict[str, tk.Button] = {}
        for name, data in CATEGORIES.items():
            label = f"{data['icon']} {name}"
            b = tk.Button(
                self.cat_row, text=label, font=self.font_btn,
                relief="flat", cursor="hand2", bd=0, padx=12, pady=8,
                command=lambda n=name: self._select_category(n)
            )
            b.pack(side="left", padx=3)
            self.cat_btns[name] = b

        # ── Converter Card ──────────────────────
        self.frm_conv = tk.LabelFrame(self.main, text=" CONVERSION ", font=self.font_label, bd=1, relief="flat")
        self.frm_conv.pack(fill="x", **P)

        # FROM row
        self.frm_from_row = tk.Frame(self.frm_conv)
        self.frm_from_row.pack(fill="x", padx=12, pady=(14, 4))
        tk.Label(self.frm_from_row, text="FROM", font=self.font_label).pack(side="left")
        self.from_var = tk.StringVar()
        self.combo_from = ttk.Combobox(self.frm_from_row, textvariable=self.from_var,
                                        state="readonly", font=self.font_btn, width=18)
        self.combo_from.pack(side="right")
        self.combo_from.bind("<<ComboboxSelected>>", lambda e: self._live_convert())

        # Value input row
        self.frm_val_row = tk.Frame(self.frm_conv)
        self.frm_val_row.pack(fill="x", padx=12, pady=4)
        self.lbl_sym = tk.Label(self.frm_val_row, text="", font=("Courier New", 12, "bold"), width=4, anchor="w")
        self.lbl_sym.pack(side="left")
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.frm_val_row, textvariable=self.entry_var,
                              font=self.font_input, relief="flat", bd=0, justify="right", width=14)
        self.entry.pack(side="right", ipady=8, padx=(0, 2))
        self.entry_var.trace_add("write", lambda *a: self._live_convert())

        # Swap row
        self.frm_swap_row = tk.Frame(self.frm_conv)
        self.frm_swap_row.pack(fill="x", padx=12, pady=2)
        self.btn_swap = tk.Button(
            self.frm_swap_row, text="⇅  SWAP UNITS", font=("Courier New", 8, "bold"),
            relief="flat", cursor="hand2", bd=0, padx=10, pady=5,
            command=self._swap_units
        )
        self.btn_swap.pack(side="left")

        # TO row
        self.frm_to_row = tk.Frame(self.frm_conv)
        self.frm_to_row.pack(fill="x", padx=12, pady=(4, 14))
        tk.Label(self.frm_to_row, text="TO", font=self.font_label).pack(side="left")
        self.to_var = tk.StringVar()
        self.combo_to = ttk.Combobox(self.frm_to_row, textvariable=self.to_var,
                                      state="readonly", font=self.font_btn, width=18)
        self.combo_to.pack(side="right")
        self.combo_to.bind("<<ComboboxSelected>>", lambda e: self._live_convert())

        # ── Result ──────────────────────────────
        self.frm_result = tk.LabelFrame(self.main, text=" RESULT ", font=self.font_label, bd=1, relief="flat")
        self.frm_result.pack(fill="x", **P)

        self.lbl_result = tk.Label(self.frm_result, text="—", font=self.font_result, anchor="center")
        self.lbl_result.pack(fill="x", padx=16, pady=(16, 4))
        self.lbl_formula = tk.Label(self.frm_result, text="", font=self.font_small, anchor="center")
        self.lbl_formula.pack(fill="x", padx=16, pady=(0, 14))

        # ── Buttons ─────────────────────────────
        self.btn_convert = tk.Button(
            self.main, text="▶  CONVERT", font=self.font_btn,
            relief="flat", cursor="hand2", bd=0, padx=20, pady=12,
            command=self._do_convert
        )
        self.btn_convert.pack(fill="x", padx=20, pady=(6, 2))

        self.btn_clear = tk.Button(
            self.main, text="✕  CLEAR INPUT", font=("Courier New", 8, "bold"),
            relief="flat", cursor="hand2", bd=0, padx=12, pady=6,
            command=self._clear
        )
        self.btn_clear.pack(fill="x", padx=20, pady=(0, 4))

        # ── History ─────────────────────────────
        self.frm_hist = tk.LabelFrame(self.main, text=" HISTORY ", font=self.font_label, bd=1, relief="flat")
        self.frm_hist.pack(fill="x", padx=20, pady=(8, 4))

        self.hist_body = tk.Frame(self.frm_hist)
        self.hist_body.pack(fill="x", padx=6, pady=6)

        self.btn_clrhist = tk.Button(
            self.frm_hist, text="Clear History", font=("Courier New", 8),
            relief="flat", cursor="hand2", bd=0, padx=8, pady=4,
            command=self._clear_history
        )
        self.btn_clrhist.pack(anchor="e", padx=8, pady=(0, 6))

        # ── Footer ──────────────────────────────
        self.lbl_footer = tk.Label(
            self.main, text="Python · Tkinter  •  Temperature · Length · Weight",
            font=("Courier New", 8)
        )
        self.lbl_footer.pack(pady=(4, 16))

        # collect all frames for theming
        self._inner_frames = [self.frm_from_row, self.frm_val_row,
                               self.frm_swap_row, self.frm_to_row, self.cat_row]

    # ── Theme ──────────────────────────────────
    def _toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self._apply_theme()

    def _apply_theme(self):
        t = self._t()
        is_dark = self.theme_name == "dark"
        self.btn_theme.config(text="☀ LIGHT" if is_dark else "🌙 DARK")

        # ttk styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TCombobox",
            fieldbackground=t["input_bg"], background=t["card"],
            foreground=t["text"], selectbackground=t["accent"],
            selectforeground=t["bg"], bordercolor=t["border"], arrowcolor=t["accent"],
        )
        style.map("TCombobox",
            fieldbackground=[("readonly", t["input_bg"])],
            foreground=[("readonly", t["text"])],
        )
        style.configure("Vertical.TScrollbar",
            background=t["panel"], troughcolor=t["bg"], arrowcolor=t["accent"])

        self.root.configure(bg=t["bg"])
        self.canvas.configure(bg=t["bg"])
        self.main.configure(bg=t["bg"])
        self.frm_header.configure(bg=t["panel"])
        self.frm_sep.configure(bg=t["border"])
        self.hist_body.configure(bg=t["card"])

        # LabelFrames
        for f in [self.frm_cat, self.frm_conv, self.frm_result, self.frm_hist]:
            f.configure(bg=t["card"], fg=t["accent"])

        # Inner frames
        for f in self._inner_frames:
            f.configure(bg=t["card"])
            for child in f.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=t["card"], fg=t["text_dim"])

        # Named widgets
        self.lbl_title.configure(bg=t["panel"], fg=t["accent"])
        self.lbl_result.configure(bg=t["card"], fg=t["accent"])
        self.lbl_formula.configure(bg=t["card"], fg=t["text_dim"])
        self.lbl_sym.configure(bg=t["card"], fg=t["accent"])
        self.lbl_footer.configure(bg=t["bg"], fg=t["text_muted"])
        self.entry.configure(bg=t["input_bg"], fg=t["text"], insertbackground=t["accent"])
        self.frm_result.configure(bg=t["card"])

        self.btn_theme.configure(bg=t["panel"], fg=t["text_dim"],
                                  activebackground=t["hover"], activeforeground=t["accent"])
        self.btn_swap.configure(bg=t["card"], fg=t["accent"],
                                 activebackground=t["hover"], activeforeground=t["accent"])
        self.btn_convert.configure(bg=t["accent"], fg=t["bg"],
                                    activebackground=t["accent_dim"], activeforeground=t["bg"])
        self.btn_clear.configure(bg=t["card"], fg=t["text_dim"],
                                  activebackground=t["hover"], activeforeground=t["error"])
        self.btn_clrhist.configure(bg=t["card"], fg=t["text_muted"],
                                    activebackground=t["hover"], activeforeground=t["error"])

        # Category buttons
        for name, btn in self.cat_btns.items():
            if name == self.selected_cat:
                btn.configure(bg=t["accent"], fg=t["bg"], activebackground=t["accent_dim"])
            else:
                btn.configure(bg=t["border"], fg=t["text_dim"],
                               activebackground=t["hover"], activeforeground=t["text"])

        self._refresh_history_ui()

    # ── Category ───────────────────────────────
    def _select_category(self, name: str):
        self.selected_cat = name
        self._on_category_change()
        self._apply_theme()

    def _on_category_change(self):
        cat = CATEGORIES[self.selected_cat]
        units = cat["units"]
        self.combo_from["values"] = units
        self.combo_to["values"] = units
        self.from_var.set(units[0])
        self.to_var.set(units[1] if len(units) > 1 else units[0])
        self._update_sym()
        self.lbl_result.config(text="—")
        self.lbl_formula.config(text="")

    def _update_sym(self):
        syms = CATEGORIES[self.selected_cat]["symbols"]
        self.lbl_sym.config(text=syms.get(self.from_var.get(), ""))

    # ── Conversion ─────────────────────────────
    def _live_convert(self):
        self._update_sym()
        raw = self.entry_var.get().strip()
        if not raw:
            self.lbl_result.config(text="—")
            self.lbl_formula.config(text="")
            return
        try:
            value = float(raw)
        except ValueError:
            return
        self._run_conversion(value, add_history=False)

    def _do_convert(self):
        raw = self.entry_var.get().strip()
        if not raw:
            self._show_error("Please enter a value.")
            return
        try:
            value = float(raw)
        except ValueError:
            self._show_error("Invalid input — please enter a number.")
            return
        self._run_conversion(value, add_history=True)

    def _run_conversion(self, value: float, add_history: bool):
        cat = CATEGORIES[self.selected_cat]
        from_u = self.from_var.get()
        to_u   = self.to_var.get()
        syms   = cat["symbols"]

        if from_u == to_u:
            result = value
        else:
            try:
                result = cat["converter"](value, from_u, to_u)
            except Exception as e:
                self._show_error(str(e))
                return

        from_s = syms.get(from_u, "")
        to_s   = syms.get(to_u, "")

        # Smart number formatting
        if abs(result) >= 1_000_000 or (result != 0 and abs(result) < 0.0001):
            res_str = f"{result:.4e}"
        elif result == int(result):
            res_str = f"{int(result):,}"
        else:
            res_str = f"{result:,.6f}".rstrip("0").rstrip(".")

        val_str = f"{value:g}"
        display = f"{val_str} {from_s}  =  {res_str} {to_s}"
        formula = f"{from_u}  →  {to_u}"

        t = self._t()
        self.lbl_result.config(text=display, fg=t["accent"])
        self.lbl_formula.config(text=formula, fg=t["text_dim"])

        if add_history:
            ts = datetime.now().strftime("%H:%M:%S")
            self.history.insert(0, f"[{ts}]  {display}")
            if len(self.history) > 15:
                self.history = self.history[:15]
            self._refresh_history_ui()

    def _show_error(self, msg: str):
        t = self._t()
        self.lbl_result.config(text=f"⚠  {msg}", fg=t["error"])
        self.lbl_formula.config(text="")

    # ── Swap ───────────────────────────────────
    def _swap_units(self):
        f, to = self.from_var.get(), self.to_var.get()
        self.from_var.set(to)
        self.to_var.set(f)
        self._update_sym()
        self._live_convert()

    # ── Clear ──────────────────────────────────
    def _clear(self):
        self.entry_var.set("")
        t = self._t()
        self.lbl_result.config(text="—", fg=t["accent"])
        self.lbl_formula.config(text="")

    # ── History ────────────────────────────────
    def _refresh_history_ui(self):
        t = self._t()
        for w in self.hist_body.winfo_children():
            w.destroy()

        if not self.history:
            tk.Label(self.hist_body, text="No conversions yet.",
                     font=self.font_hist, bg=t["card"], fg=t["text_muted"]).pack(pady=8)
            return

        for i, entry in enumerate(self.history):
            bg = t["card"] if i % 2 == 0 else t["hover"]
            row = tk.Frame(self.hist_body, bg=bg)
            row.pack(fill="x")
            tk.Label(row, text=entry, font=self.font_hist,
                     bg=bg, fg=t["text_dim"], anchor="w", padx=8, pady=3).pack(fill="x")

    def _clear_history(self):
        self.history.clear()
        self._refresh_history_ui()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

def main():
    root = tk.Tk()
    UnitConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()