"""
Spot the Difference — GUI Layout (Tkinter)
Matches the visualised mockup: toolbar → stats bar → side-by-side canvases → status bar.
Run standalone to preview all three game states with demo data.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from enum import Enum, auto


# ──────────────────────────────────────────────
#  Colour palette (mirrors the mockup)
# ──────────────────────────────────────────────
C = {
    "bg":          "#f5f5f3",   # window background
    "surface":     "#ffffff",   # toolbar / stats bar / status bar
    "canvas_bg":   "#2a2a2a",   # image canvas background
    "border":      "#e0ddd8",   # separator lines
    "text":        "#1a1a1a",   # primary text
    "muted":       "#6b7280",   # secondary / label text
    "hint":        "#9ca3af",   # tertiary / hint text

    "blue":        "#185FA5",   # Remaining counter
    "blue_bg":     "#e6f1fb",
    "blue_label":  "#0C447C",

    "red":         "#A32D2D",   # Mistakes
    "red_bg":      "#fcebeb",
    "red_label":   "#791F1F",

    "green":       "#3B6D11",   # Found / success
    "green_bg":    "#eaf3de",
    "green_label": "#27500A",

    "teal":        "#0F6E56",   # Reveal button accent
    "teal_bg":     "#E1F5EE",
    "teal_border": "#5DCAA5",

    "orig_bg":     "#E1F5EE",   # Original label badge
    "orig_fg":     "#085041",
    "mod_bg":      "#E6F1FB",   # Modified label badge
    "mod_fg":      "#0C447C",

    "statusdot_ok":   "#28c840",
    "statusdot_warn": "#febc2e",
    "statusdot_err":  "#A32D2D",
}

CANVAS_W = 560   # width of each image canvas (px)
CANVAS_H = 380   # height of each image canvas (px)
FONT = ("Segoe UI", 10)


# ──────────────────────────────────────────────
#  Game state enum
# ──────────────────────────────────────────────
class State(Enum):
    NO_IMAGE   = auto()   # nothing loaded yet
    PLAYING    = auto()   # active round
    GAME_OVER  = auto()   # 3 mistakes reached
    VICTORY    = auto()   # all 5 found


# ──────────────────────────────────────────────
#  Helper widgets
# ──────────────────────────────────────────────
class StatCell(tk.Frame):
    """A single metric in the stats bar: icon label · value."""

    def __init__(self, parent, label: str, value: str, value_color: str, **kw):
        super().__init__(parent, bg=C["surface"], **kw)
        self._var = tk.StringVar(value=value)

        self.lbl = tk.Label(self, text=label, font=("Segoe UI", 9),
                            fg=C["muted"], bg=C["surface"])
        self.lbl.pack(side=tk.LEFT, padx=(0, 4))

        self.val = tk.Label(self, textvariable=self._var,
                            font=("Segoe UI", 13, "bold"),
                            fg=value_color, bg=C["surface"])
        self.val.pack(side=tk.LEFT)

        # right border separator (drawn by parent as needed)

    def set(self, text: str):
        self._var.set(text)

    def set_color(self, color: str):
        self.val.config(fg=color)


class CanvasPanel(tk.Frame):
    """Label strip + tk.Canvas for one image (original or modified)."""

    def __init__(self, parent, badge_text: str, badge_bg: str, badge_fg: str,
                 hint: str, clickable: bool = False, **kw):
        super().__init__(parent, bg=C["surface"], **kw)
        self._clickable = clickable

        # ── label strip ──────────────────────────────
        strip = tk.Frame(self, bg=C["surface"],
                         highlightbackground=C["border"], highlightthickness=1)
        strip.pack(fill=tk.X)

        tk.Label(strip, text=badge_text,
                 font=("Segoe UI", 9, "bold"),
                 fg=badge_fg, bg=badge_bg,
                 padx=7, pady=2,
                 relief=tk.FLAT).pack(side=tk.LEFT, padx=8, pady=4)

        tk.Label(strip, text=hint,
                 font=("Segoe UI", 9),
                 fg=C["hint"], bg=C["surface"]).pack(side=tk.LEFT)

        # ── canvas ───────────────────────────────────
        cursor = "crosshair" if clickable else "arrow"
        self.canvas = tk.Canvas(self,
                                width=CANVAS_W, height=CANVAS_H,
                                bg=C["canvas_bg"],
                                highlightthickness=0,
                                cursor=cursor)
        self.canvas.pack()
        self._draw_placeholder()

    def _draw_placeholder(self):
        """Neutral placeholder shown before an image is loaded."""
        cx, cy = CANVAS_W // 2, CANVAS_H // 2
        self.canvas.create_rectangle(cx - 60, cy - 45, cx + 60, cy + 45,
                                     outline="#555", width=1)
        self.canvas.create_line(cx - 60, cy - 45, cx + 60, cy + 45,
                                fill="#555", width=1)
        self.canvas.create_line(cx + 60, cy - 45, cx - 60, cy + 45,
                                fill="#555", width=1)
        self.canvas.create_text(cx, cy + 65,
                                text="No image loaded",
                                fill="#666", font=("Segoe UI", 10))

    def clear_placeholder(self):
        self.canvas.delete("all")

    def lock(self):
        """Remove click binding and switch to arrow cursor."""
        self.canvas.config(cursor="arrow")
        self.canvas.unbind("<Button-1>")

    def unlock(self, callback):
        """Restore crosshair and bind click handler."""
        self.canvas.config(cursor="crosshair")
        self.canvas.bind("<Button-1>", callback)


# ──────────────────────────────────────────────
#  Main GUI class
# ──────────────────────────────────────────────
class GameGUI(tk.Tk):
    """
    Top-level Tkinter window.

    Layout (top → bottom):
        ┌─────────────────────────────────────────┐
        │  Toolbar  (Load · Reveal)               │
        ├─────────────────────────────────────────┤
        │  Stats bar  (Remaining · Mistakes · …)  │
        ├────────────────┬────────────────────────┤
        │ Original panel │  Modified panel        │
        │ (left, locked) │  (right, clickable)    │
        ├─────────────────────────────────────────┤
        │  Status bar                             │
        └─────────────────────────────────────────┘
    """

    MAX_MISTAKES = 3
    TOTAL_DIFFS  = 5

    def __init__(self):
        super().__init__()
        self.title("Spot the Difference")
        self.resizable(False, False)
        self.configure(bg=C["bg"])

        # ── game state variables ──────────────────
        self._state        = State.NO_IMAGE
        self._remaining    = tk.IntVar(value=self.TOTAL_DIFFS)
        self._mistakes     = tk.IntVar(value=0)
        self._found        = tk.IntVar(value=0)
        self._total_mis    = tk.IntVar(value=0)
        self._image_name   = tk.StringVar(value="—")

        # Tkinter image references (prevent GC)
        self._orig_photo   = None
        self._mod_photo    = None

        self._build_ui()
        self._refresh_state()

    # ─────────────────────────────────────────────
    #  UI construction
    # ─────────────────────────────────────────────
    def _build_ui(self):
        self._build_toolbar()
        self._build_separator()
        self._build_statsbar()
        self._build_separator()
        self._build_canvases()
        self._build_separator()
        self._build_statusbar()

    def _build_toolbar(self):
        bar = tk.Frame(self, bg=C["surface"], pady=6, padx=10)
        bar.pack(fill=tk.X)

        # Load image button
        self._btn_load = tk.Button(
            bar,
            text="⊞  Load image",
            font=("Segoe UI", 10),
            fg=C["text"], bg=C["surface"],
            activebackground=C["bg"],
            relief=tk.FLAT,
            bd=0,
            padx=10, pady=4,
            cursor="hand2",
            command=self._on_load,
        )
        self._btn_load.pack(side=tk.LEFT, padx=(0, 6))
        _add_flat_border(self._btn_load, C["border"])

        # Reveal button
        self._btn_reveal = tk.Button(
            bar,
            text="◎  Reveal all",
            font=("Segoe UI", 10),
            fg=C["teal"], bg=C["surface"],
            activebackground=C["teal_bg"],
            relief=tk.FLAT,
            bd=0,
            padx=10, pady=4,
            cursor="hand2",
            command=self._on_reveal,
        )
        self._btn_reveal.pack(side=tk.LEFT)
        _add_flat_border(self._btn_reveal, C["teal_border"])

        # Filename label (right-aligned)
        self._lbl_file = tk.Label(
            bar,
            textvariable=self._image_name,
            font=("Segoe UI", 9),
            fg=C["hint"], bg=C["surface"],
        )
        self._lbl_file.pack(side=tk.RIGHT, padx=4)

        # Notification banner (hidden by default)
        self._banner = tk.Label(
            bar,
            text="",
            font=("Segoe UI", 9),
            pady=3, padx=10,
        )

    def _build_statsbar(self):
        bar = tk.Frame(self, bg=C["surface"])
        bar.pack(fill=tk.X)

        def sep():
            tk.Frame(bar, bg=C["border"], width=1).pack(
                side=tk.LEFT, fill=tk.Y, padx=0, pady=6)

        cells = [
            ("Remaining",     self._remaining_str,  C["blue"]),
            ("Mistakes",      self._mistakes_str,   C["red"]),
            ("Found",         self._found_str,      C["green"]),
        ]

        for label, strvar, color in cells:
            f = tk.Frame(bar, bg=C["surface"], padx=14, pady=6)
            f.pack(side=tk.LEFT)
            tk.Label(f, text=label, font=("Segoe UI", 9),
                     fg=C["muted"], bg=C["surface"]).pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(f, textvariable=strvar, font=("Segoe UI", 13, "bold"),
                     fg=color, bg=C["surface"]).pack(side=tk.LEFT)
            sep()

        # Total mistakes — right-aligned
        f = tk.Frame(bar, bg=C["surface"], padx=14, pady=6)
        f.pack(side=tk.RIGHT)
        tk.Label(f, text="Total mistakes", font=("Segoe UI", 9),
                 fg=C["muted"], bg=C["surface"]).pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(f, textvariable=self._total_mis_str,
                 font=("Segoe UI", 13, "bold"),
                 fg=C["text"], bg=C["surface"]).pack(side=tk.LEFT)

        self._statsbar = bar

    def _build_canvases(self):
        outer = tk.Frame(self, bg=C["border"])
        outer.pack(fill=tk.BOTH, expand=True)

        self._orig_panel = CanvasPanel(
            outer,
            badge_text="Original",
            badge_bg=C["orig_bg"],
            badge_fg=C["orig_fg"],
            hint="reference only — not clickable",
            clickable=False,
        )
        self._orig_panel.pack(side=tk.LEFT)

        # vertical divider
        tk.Frame(outer, bg=C["border"], width=1).pack(
            side=tk.LEFT, fill=tk.Y)

        self._mod_panel = CanvasPanel(
            outer,
            badge_text="Modified",
            badge_bg=C["mod_bg"],
            badge_fg=C["mod_fg"],
            hint="click here to find differences",
            clickable=True,
        )
        self._mod_panel.pack(side=tk.LEFT)

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=C["surface"], padx=12, pady=6)
        bar.pack(fill=tk.X)

        self._dot = tk.Label(bar, text="●", font=("Segoe UI", 8),
                             fg=C["statusdot_warn"], bg=C["surface"])
        self._dot.pack(side=tk.LEFT, padx=(0, 6))

        self._status_lbl = tk.Label(
            bar, text="Load an image to start playing.",
            font=("Segoe UI", 9), fg=C["muted"], bg=C["surface"],
        )
        self._status_lbl.pack(side=tk.LEFT)

    def _build_separator(self):
        tk.Frame(self, bg=C["border"], height=1).pack(fill=tk.X)

    # ─────────────────────────────────────────────
    #  Derived StringVars for stats bar
    # ─────────────────────────────────────────────
    @property
    def _remaining_str(self):
        if not hasattr(self, "_sv_rem"):
            self._sv_rem = tk.StringVar()
        self._sv_rem.set(str(self._remaining.get()))
        return self._sv_rem

    @property
    def _mistakes_str(self):
        if not hasattr(self, "_sv_mis"):
            self._sv_mis = tk.StringVar()
        self._sv_mis.set(f"{self._mistakes.get()} / {self.MAX_MISTAKES}")
        return self._sv_mis

    @property
    def _found_str(self):
        if not hasattr(self, "_sv_fnd"):
            self._sv_fnd = tk.StringVar()
        self._sv_fnd.set(f"{self._found.get()} / {self.TOTAL_DIFFS}")
        return self._sv_fnd

    @property
    def _total_mis_str(self):
        if not hasattr(self, "_sv_tot"):
            self._sv_tot = tk.StringVar()
        self._sv_tot.set(str(self._total_mis.get()))
        return self._sv_tot

    def _sync_stat_vars(self):
        self._sv_rem.set(str(self._remaining.get()))
        self._sv_mis.set(f"{self._mistakes.get()} / {self.MAX_MISTAKES}")
        self._sv_fnd.set(f"{self._found.get()} / {self.TOTAL_DIFFS}")
        self._sv_tot.set(str(self._total_mis.get()))

    # ─────────────────────────────────────────────
    #  State transitions
    # ─────────────────────────────────────────────
    def _refresh_state(self):
        """Apply all visual changes that correspond to the current game state."""
        s = self._state

        # ── Remaining colour ─────────────────────
        rem_color = C["green"] if self._remaining.get() == 0 else C["blue"]

        # ── Load button always enabled ────────────
        self._btn_load.config(state=tk.NORMAL, cursor="hand2")

        if s == State.NO_IMAGE:
            self._btn_reveal.config(state=tk.DISABLED, cursor="arrow",
                                    fg=C["hint"])
            self._set_status("Load an image to start playing.", C["statusdot_warn"])
            self._hide_banner()

        elif s == State.PLAYING:
            self._btn_reveal.config(state=tk.NORMAL, cursor="hand2",
                                    fg=C["teal"])
            self._mod_panel.unlock(self._on_canvas_click)
            self._set_status(
                "Click on the right image to find differences.",
                C["statusdot_ok"])
            self._hide_banner()

        elif s == State.GAME_OVER:
            self._btn_reveal.config(state=tk.DISABLED, cursor="arrow",
                                    fg=C["hint"])
            self._mod_panel.lock()
            self._set_status(
                "Maximum mistakes reached — load a new image to continue.",
                C["statusdot_err"])
            self._show_banner(
                f"  ⚠  Too many mistakes — load a new image",
                bg=C["red_bg"], fg=C["red_label"], border=C["red"])
            self._draw_gameover_overlay()

        elif s == State.VICTORY:
            self._btn_reveal.config(state=tk.DISABLED, cursor="arrow",
                                    fg=C["hint"])
            self._btn_load.config(text="⊞  Load next image")
            self._mod_panel.lock()
            self._set_status(
                "Congratulations — all 5 differences found! Load a new image to keep playing.",
                C["statusdot_ok"])
            self._show_banner(
                f"  ✓  All {self.TOTAL_DIFFS} found! Load a new image to continue",
                bg=C["green_bg"], fg=C["green_label"], border="#97C459")

        self._sync_stat_vars()

    def _set_status(self, text: str, dot_color: str):
        self._dot.config(fg=dot_color)
        self._status_lbl.config(text=text)

    def _show_banner(self, text: str, bg: str, fg: str, border: str):
        self._banner.config(text=text, bg=bg, fg=fg,
                            highlightbackground=border,
                            highlightthickness=1)
        self._banner.pack(side=tk.RIGHT, padx=8)

    def _hide_banner(self):
        self._banner.pack_forget()

    # ─────────────────────────────────────────────
    #  Canvas drawing helpers
    # ─────────────────────────────────────────────
    def draw_image(self, canvas: tk.Canvas, photo_image):
        """Display a PhotoImage centred on the given canvas."""
        canvas.delete("all")
        canvas.create_image(CANVAS_W // 2, CANVAS_H // 2,
                            anchor=tk.CENTER, image=photo_image)

    def draw_found_circle(self, x: int, y: int, r: int):
        """Draw a red found-circle on BOTH canvases at the same location."""
        for canvas in (self._orig_panel.canvas, self._mod_panel.canvas):
            canvas.create_oval(x - r, y - r, x + r, y + r,
                               outline="#e53935", width=3, tags="marker")

    def draw_reveal_circle(self, x: int, y: int, r: int):
        """Draw a blue reveal-circle on BOTH canvases."""
        for canvas in (self._orig_panel.canvas, self._mod_panel.canvas):
            canvas.create_oval(x - r, y - r, x + r, y + r,
                               outline="#1565C0", width=3, tags="marker")

    def draw_wrong_click(self, x: int, y: int):
        """Draw a small red ✕ on the modified canvas at a wrong-click location."""
        s = 7
        self._mod_panel.canvas.create_line(
            x - s, y - s, x + s, y + s,
            fill="#e53935", width=2, tags="marker")
        self._mod_panel.canvas.create_line(
            x + s, y - s, x - s, y + s,
            fill="#e53935", width=2, tags="marker")

    def _draw_gameover_overlay(self):
        """Semi-transparent red tint + badge over the modified canvas."""
        c = self._mod_panel.canvas
        c.create_rectangle(0, 0, CANVAS_W, CANVAS_H,
                           fill="#A32D2D", stipple="gray25",
                           outline="", tags="overlay")
        cx, cy = CANVAS_W // 2, CANVAS_H // 2
        c.create_rectangle(cx - 110, cy - 18, cx + 110, cy + 18,
                           fill="#A32D2D", outline="", tags="overlay")
        c.create_text(cx, cy,
                      text="Game over — 3 mistakes",
                      fill="#FCEBEB", font=("Segoe UI", 11, "bold"),
                      tags="overlay")

    def refresh_canvases(self):
        """
        Called by ImageProcessor after marking differences.
        Re-draws both PhotoImages onto their canvases.
        Replace self._orig_photo / self._mod_photo before calling.
        """
        if self._orig_photo:
            self.draw_image(self._orig_panel.canvas, self._orig_photo)
        if self._mod_photo:
            self.draw_image(self._mod_panel.canvas, self._mod_photo)

    # ─────────────────────────────────────────────
    #  Event handlers (stubs — wired up to game logic)
    # ─────────────────────────────────────────────
    def _on_load(self):
        """
        Open a file dialog and hand the path to ImageProcessor.
        Replace the body of this method with real game logic.
        """
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files",   "*.*"),
            ],
        )
        if not path:
            return

        import os
        self._image_name.set(os.path.basename(path))
        self._btn_load.config(text="⊞  Load image")

        # Reset per-image state
        self._remaining.set(self.TOTAL_DIFFS)
        self._mistakes.set(0)
        self._found.set(0)
        self._state = State.PLAYING

        self._orig_panel.clear_placeholder()
        self._mod_panel.clear_placeholder()
        self._mod_panel.canvas.delete("overlay")

        self._refresh_state()

        # ── Hook for ImageProcessor ───────────────────────────────────────
        # image_processor.load(path)
        # self._orig_photo = image_processor.to_tk_image(image_processor.original)
        # self._mod_photo  = image_processor.to_tk_image(image_processor.modified)
        # self.refresh_canvases()
        # game_state.reset(image_processor.differences)
        # ──────────────────────────────────────────────────────────────────

        # DEMO: draw grey placeholder so layout is clear
        self._orig_panel.canvas.create_text(
            CANVAS_W // 2, CANVAS_H // 2,
            text=f"Original image\n{os.path.basename(path)}",
            fill="#aaa", font=("Segoe UI", 11), justify=tk.CENTER)
        self._mod_panel.canvas.create_text(
            CANVAS_W // 2, CANVAS_H // 2,
            text=f"Modified image\n(5 hidden differences)",
            fill="#aaa", font=("Segoe UI", 11), justify=tk.CENTER)

    def _on_reveal(self):
        """
        Mark all unfound differences in blue on both canvases.
        Replace with: game_state.unfound() → draw_reveal_circle() for each.
        """
        if self._state != State.PLAYING:
            return
        answer = messagebox.askyesno(
            "Reveal",
            "Reveal all unfound differences?\nYou will need to load a new image.",
        )
        if not answer:
            return

        # ── Hook for game logic ───────────────────────────────────────────
        # for diff in game_state.unfound():
        #     cx, cy = diff.center()
        #     self.draw_reveal_circle(cx, cy, diff.radius())
        # ─────────────────────────────────────────────────────────────────

        # DEMO: draw three placeholder reveal circles
        for cx, cy in [(140, 130), (280, 200), (430, 110)]:
            self.draw_reveal_circle(cx, cy, 30)

        self._state = State.GAME_OVER
        self._refresh_state()

    def _on_canvas_click(self, event):
        """
        Fired when player clicks on the modified canvas.
        Replace with: result = game_state.check_click(event.x, event.y)
        """
        if self._state != State.PLAYING:
            return

        x, y = event.x, event.y

        # ── Hook for game logic ───────────────────────────────────────────
        # diff = game_state.check_click(x, y)
        # if diff:
        #     self.draw_found_circle(diff.cx, diff.cy, diff.radius())
        #     self._found.set(game_state.found_count())
        #     self._remaining.set(game_state.remaining())
        #     self._sync_stat_vars()
        #     if game_state.remaining() == 0:
        #         self._state = State.VICTORY
        #         self._refresh_state()
        #         messagebox.showinfo("You win!", "All 5 differences found!")
        # else:
        #     self.draw_wrong_click(x, y)
        #     self._total_mis.set(self._total_mis.get() + 1)
        #     new_mis = self._mistakes.get() + 1
        #     self._mistakes.set(new_mis)
        #     self._sync_stat_vars()
        #     if new_mis >= self.MAX_MISTAKES:
        #         self._state = State.GAME_OVER
        #         self._refresh_state()
        # ─────────────────────────────────────────────────────────────────

        # DEMO toggle: alternate correct / wrong for testing
        if not hasattr(self, "_demo_toggle"):
            self._demo_toggle = 0
        self._demo_toggle += 1

        if self._demo_toggle % 2 == 1:
            # Simulate a correct click
            self.draw_found_circle(x, y, 28)
            found = self._found.get() + 1
            self._found.set(found)
            self._remaining.set(self.TOTAL_DIFFS - found)
            self._sync_stat_vars()
            if found >= self.TOTAL_DIFFS:
                self._state = State.VICTORY
                self._refresh_state()
                messagebox.showinfo(
                    "Congratulations!",
                    "You found all 5 differences!\nLoad a new image to continue.")
        else:
            # Simulate a wrong click
            self.draw_wrong_click(x, y)
            mis = self._mistakes.get() + 1
            self._mistakes.set(mis)
            self._total_mis.set(self._total_mis.get() + 1)
            self._sync_stat_vars()
            if mis >= self.MAX_MISTAKES:
                self._state = State.GAME_OVER
                self._refresh_state()


# ──────────────────────────────────────────────
#  Utility: flat-border simulation via highlight
# ──────────────────────────────────────────────
def _add_flat_border(widget: tk.Widget, color: str):
    """Simulate a 1px border on a borderless button using highlightthickness."""
    widget.config(
        highlightbackground=color,
        highlightcolor=color,
        highlightthickness=1,
    )


# ──────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = GameGUI()
    app.mainloop()
