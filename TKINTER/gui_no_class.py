"""
Spot the Difference — GUI Layout (functions only, no classes)
All state lives in module-level variables.
All behaviour lives in def functions.
Run with: python gui_no_class.py
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox

# ──────────────────────────────────────────────
#  Colour palette
# ──────────────────────────────────────────────
C = {
    "bg":          "#f5f5f3",
    "surface":     "#ffffff",
    "canvas_bg":   "#2a2a2a",
    "border":      "#e0ddd8",
    "text":        "#1a1a1a",
    "muted":       "#6b7280",
    "hint":        "#9ca3af",
    "blue":        "#185FA5",
    "red":         "#A32D2D",
    "red_bg":      "#fcebeb",
    "red_label":   "#791F1F",
    "green":       "#3B6D11",
    "green_bg":    "#eaf3de",
    "green_label": "#27500A",
    "teal":        "#0F6E56",
    "teal_bg":     "#E1F5EE",
    "teal_border": "#5DCAA5",
    "orig_bg":     "#E1F5EE",
    "orig_fg":     "#085041",
    "mod_bg":      "#E6F1FB",
    "mod_fg":      "#0C447C",
    "dot_ok":      "#28c840",
    "dot_warn":    "#febc2e",
    "dot_err":     "#A32D2D",
}

CANVAS_W   = 560
CANVAS_H   = 380
MAX_MIS    = 3
TOTAL_DIFFS = 5

# ──────────────────────────────────────────────
#  Global state  (replaces self.x on a class)
# ──────────────────────────────────────────────
state = {
    "game":       "no_image",   # "no_image" | "playing" | "game_over" | "victory"
    "remaining":  TOTAL_DIFFS,
    "mistakes":   0,
    "found":      0,
    "total_mis":  0,
    "demo_toggle": 0,
}

# Widget references — populated in build_ui()
widgets = {}

# Tkinter StringVars — populated in build_ui()
sv = {}


# ──────────────────────────────────────────────
#  Stats helpers
# ──────────────────────────────────────────────
def sync_stats():
    sv["remaining"].set(str(state["remaining"]))
    sv["mistakes"].set(f"{state['mistakes']} / {MAX_MIS}")
    sv["found"].set(f"{state['found']} / {TOTAL_DIFFS}")
    sv["total_mis"].set(str(state["total_mis"]))


# ──────────────────────────────────────────────
#  State transitions
# ──────────────────────────────────────────────
def refresh_state():
    """Update every widget to match the current game state."""
    g = state["game"]

    widgets["btn_load"].config(state=tk.NORMAL, cursor="hand2")

    if g == "no_image":
        widgets["btn_reveal"].config(state=tk.DISABLED, cursor="arrow",
                                     fg=C["hint"])
        set_status("Load an image to start playing.", C["dot_warn"])
        hide_banner()

    elif g == "playing":
        widgets["btn_reveal"].config(state=tk.NORMAL, cursor="hand2",
                                     fg=C["teal"])
        widgets["mod_canvas"].config(cursor="crosshair")
        widgets["mod_canvas"].bind("<Button-1>", on_canvas_click)
        set_status("Click on the right image to find differences.", C["dot_ok"])
        hide_banner()

    elif g == "game_over":
        widgets["btn_reveal"].config(state=tk.DISABLED, cursor="arrow",
                                     fg=C["hint"])
        widgets["mod_canvas"].config(cursor="arrow")
        widgets["mod_canvas"].unbind("<Button-1>")
        set_status("Maximum mistakes reached — load a new image to continue.",
                   C["dot_err"])
        show_banner("  ⚠  Too many mistakes — load a new image",
                    bg=C["red_bg"], fg=C["red_label"], border=C["red"])
        draw_gameover_overlay()

    elif g == "victory":
        widgets["btn_reveal"].config(state=tk.DISABLED, cursor="arrow",
                                     fg=C["hint"])
        widgets["btn_load"].config(text="⊞  Load next image")
        widgets["mod_canvas"].config(cursor="arrow")
        widgets["mod_canvas"].unbind("<Button-1>")
        set_status(
            "Congratulations — all 5 found! Load a new image to keep playing.",
            C["dot_ok"])
        show_banner("  ✓  All 5 found! Load a new image to continue",
                    bg=C["green_bg"], fg=C["green_label"], border="#97C459")

    sync_stats()


def set_status(text, dot_color):
    widgets["dot"].config(fg=dot_color)
    widgets["status_lbl"].config(text=text)


def show_banner(text, bg, fg, border):
    widgets["banner"].config(text=text, bg=bg, fg=fg,
                             highlightbackground=border,
                             highlightthickness=1)
    widgets["banner"].pack(side=tk.RIGHT, padx=8)


def hide_banner():
    widgets["banner"].pack_forget()


# ──────────────────────────────────────────────
#  Canvas drawing
# ──────────────────────────────────────────────
def draw_found_circle(x, y, r=28):
    """Red circle on both canvases at the same position."""
    for canvas in (widgets["orig_canvas"], widgets["mod_canvas"]):
        canvas.create_oval(x - r, y - r, x + r, y + r,
                           outline="#e53935", width=3, tags="marker")


def draw_reveal_circle(x, y, r=28):
    """Blue circle on both canvases."""
    for canvas in (widgets["orig_canvas"], widgets["mod_canvas"]):
        canvas.create_oval(x - r, y - r, x + r, y + r,
                           outline="#1565C0", width=3, tags="marker")


def draw_wrong_click(x, y):
    """Small red ✕ on the modified canvas."""
    s = 7
    widgets["mod_canvas"].create_line(x - s, y - s, x + s, y + s,
                                      fill="#e53935", width=2, tags="marker")
    widgets["mod_canvas"].create_line(x + s, y - s, x - s, y + s,
                                      fill="#e53935", width=2, tags="marker")


def draw_gameover_overlay():
    c = widgets["mod_canvas"]
    cx, cy = CANVAS_W // 2, CANVAS_H // 2
    c.create_rectangle(0, 0, CANVAS_W, CANVAS_H,
                       fill="#A32D2D", stipple="gray25",
                       outline="", tags="overlay")
    c.create_rectangle(cx - 110, cy - 18, cx + 110, cy + 18,
                       fill="#A32D2D", outline="", tags="overlay")
    c.create_text(cx, cy,
                  text="Game over — 3 mistakes",
                  fill="#FCEBEB", font=("Segoe UI", 11, "bold"),
                  tags="overlay")


def draw_placeholder(canvas, text):
    cx, cy = CANVAS_W // 2, CANVAS_H // 2
    canvas.create_rectangle(cx - 60, cy - 45, cx + 60, cy + 45,
                             outline="#555", width=1)
    canvas.create_line(cx - 60, cy - 45, cx + 60, cy + 45, fill="#555", width=1)
    canvas.create_line(cx + 60, cy - 45, cx - 60, cy + 45, fill="#555", width=1)
    canvas.create_text(cx, cy + 65, text=text, fill="#666",
                       font=("Segoe UI", 10))


# ──────────────────────────────────────────────
#  Event handlers
# ──────────────────────────────────────────────
def on_load():
    path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"),
                   ("All files", "*.*")],
    )
    if not path:
        return

    sv["filename"].set(os.path.basename(path))
    widgets["btn_load"].config(text="⊞  Load image")

    # Reset per-image state
    state["remaining"]  = TOTAL_DIFFS
    state["mistakes"]   = 0
    state["found"]      = 0
    state["demo_toggle"] = 0
    state["game"]       = "playing"

    widgets["orig_canvas"].delete("all")
    widgets["mod_canvas"].delete("all")

    refresh_state()

    # ── Hook: replace these two lines with real ImageProcessor calls ──
    # image_processor.load(path)
    # orig_photo = image_processor.to_tk_image(image_processor.original)
    # mod_photo  = image_processor.to_tk_image(image_processor.modified)
    # widgets["orig_canvas"].create_image(CANVAS_W//2, CANVAS_H//2,
    #                                     anchor=tk.CENTER, image=orig_photo)
    # widgets["mod_canvas"].create_image(CANVAS_W//2, CANVAS_H//2,
    #                                    anchor=tk.CENTER, image=mod_photo)
    # ─────────────────────────────────────────────────────────────────

    # DEMO placeholders
    widgets["orig_canvas"].create_text(
        CANVAS_W // 2, CANVAS_H // 2,
        text=f"Original image\n{os.path.basename(path)}",
        fill="#aaa", font=("Segoe UI", 11), justify=tk.CENTER)
    widgets["mod_canvas"].create_text(
        CANVAS_W // 2, CANVAS_H // 2,
        text="Modified image\n(5 hidden differences)",
        fill="#aaa", font=("Segoe UI", 11), justify=tk.CENTER)


def on_reveal():
    if state["game"] != "playing":
        return
    answer = messagebox.askyesno(
        "Reveal",
        "Reveal all unfound differences?\nYou will need to load a new image.",
    )
    if not answer:
        return

    # ── Hook: replace with real game logic ────────────────────────────
    # for diff in game_state.unfound():
    #     draw_reveal_circle(diff.cx, diff.cy, diff.radius())
    # ─────────────────────────────────────────────────────────────────

    # DEMO
    for cx, cy in [(140, 130), (280, 200), (430, 110)]:
        draw_reveal_circle(cx, cy, 30)

    state["game"] = "game_over"
    refresh_state()


def on_canvas_click(event):
    if state["game"] != "playing":
        return

    x, y = event.x, event.y

    # ── Hook: replace with real game logic ────────────────────────────
    # diff = game_state.check_click(x, y)
    # if diff:
    #     draw_found_circle(diff.cx, diff.cy, diff.radius())
    #     state["found"]     += 1
    #     state["remaining"] -= 1
    #     sync_stats()
    #     if state["remaining"] == 0:
    #         state["game"] = "victory"
    #         refresh_state()
    #         messagebox.showinfo("You win!", "All 5 differences found!")
    # else:
    #     draw_wrong_click(x, y)
    #     state["mistakes"]  += 1
    #     state["total_mis"] += 1
    #     sync_stats()
    #     if state["mistakes"] >= MAX_MIS:
    #         state["game"] = "game_over"
    #         refresh_state()
    # ─────────────────────────────────────────────────────────────────

    # DEMO: alternate correct / wrong for testing
    state["demo_toggle"] += 1
    if state["demo_toggle"] % 2 == 1:
        draw_found_circle(x, y)
        state["found"]     += 1
        state["remaining"] -= 1
        sync_stats()
        if state["found"] >= TOTAL_DIFFS:
            state["game"] = "victory"
            refresh_state()
            messagebox.showinfo("Congratulations!",
                                "You found all 5 differences!\n"
                                "Load a new image to continue.")
    else:
        draw_wrong_click(x, y)
        state["mistakes"]  += 1
        state["total_mis"] += 1
        sync_stats()
        if state["mistakes"] >= MAX_MIS:
            state["game"] = "game_over"
            refresh_state()


# ──────────────────────────────────────────────
#  UI construction
# ──────────────────────────────────────────────
def build_separator(root):
    tk.Frame(root, bg=C["border"], height=1).pack(fill=tk.X)


def build_toolbar(root):
    bar = tk.Frame(root, bg=C["surface"], pady=6, padx=10)
    bar.pack(fill=tk.X)

    btn_load = tk.Button(bar, text="⊞  Load image",
                         font=("Segoe UI", 10),
                         fg=C["text"], bg=C["surface"],
                         activebackground=C["bg"],
                         relief=tk.FLAT, bd=0,
                         padx=10, pady=4,
                         cursor="hand2",
                         command=on_load)
    btn_load.pack(side=tk.LEFT, padx=(0, 6))
    btn_load.config(highlightbackground=C["border"],
                    highlightcolor=C["border"],
                    highlightthickness=1)
    widgets["btn_load"] = btn_load

    btn_reveal = tk.Button(bar, text="◎  Reveal all",
                           font=("Segoe UI", 10),
                           fg=C["teal"], bg=C["surface"],
                           activebackground=C["teal_bg"],
                           relief=tk.FLAT, bd=0,
                           padx=10, pady=4,
                           cursor="hand2",
                           command=on_reveal)
    btn_reveal.pack(side=tk.LEFT)
    btn_reveal.config(highlightbackground=C["teal_border"],
                      highlightcolor=C["teal_border"],
                      highlightthickness=1)
    widgets["btn_reveal"] = btn_reveal

    sv["filename"] = tk.StringVar(value="—")
    tk.Label(bar, textvariable=sv["filename"],
             font=("Segoe UI", 9), fg=C["hint"],
             bg=C["surface"]).pack(side=tk.RIGHT, padx=4)

    banner = tk.Label(bar, text="", font=("Segoe UI", 9), pady=3, padx=10)
    widgets["banner"] = banner


def build_statsbar(root):
    bar = tk.Frame(root, bg=C["surface"])
    bar.pack(fill=tk.X)

    def sep():
        tk.Frame(bar, bg=C["border"], width=1).pack(
            side=tk.LEFT, fill=tk.Y, pady=6)

    cells = [
        ("Remaining", "remaining", C["blue"]),
        ("Mistakes",  "mistakes",  C["red"]),
        ("Found",     "found",     C["green"]),
    ]

    sv["remaining"] = tk.StringVar(value=str(TOTAL_DIFFS))
    sv["mistakes"]  = tk.StringVar(value=f"0 / {MAX_MIS}")
    sv["found"]     = tk.StringVar(value=f"0 / {TOTAL_DIFFS}")
    sv["total_mis"] = tk.StringVar(value="0")

    for label, key, color in cells:
        f = tk.Frame(bar, bg=C["surface"], padx=14, pady=6)
        f.pack(side=tk.LEFT)
        tk.Label(f, text=label, font=("Segoe UI", 9),
                 fg=C["muted"], bg=C["surface"]).pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(f, textvariable=sv[key],
                 font=("Segoe UI", 13, "bold"),
                 fg=color, bg=C["surface"]).pack(side=tk.LEFT)
        sep()

    f = tk.Frame(bar, bg=C["surface"], padx=14, pady=6)
    f.pack(side=tk.RIGHT)
    tk.Label(f, text="Total mistakes", font=("Segoe UI", 9),
             fg=C["muted"], bg=C["surface"]).pack(side=tk.LEFT, padx=(0, 5))
    tk.Label(f, textvariable=sv["total_mis"],
             font=("Segoe UI", 13, "bold"),
             fg=C["text"], bg=C["surface"]).pack(side=tk.LEFT)


def build_canvases(root):
    outer = tk.Frame(root, bg=C["border"])
    outer.pack(fill=tk.BOTH, expand=True)

    # ── Original (left) ──────────────────────────────────────
    left = tk.Frame(outer, bg=C["surface"])
    left.pack(side=tk.LEFT)

    orig_strip = tk.Frame(left, bg=C["surface"],
                          highlightbackground=C["border"],
                          highlightthickness=1)
    orig_strip.pack(fill=tk.X)
    tk.Label(orig_strip, text="Original",
             font=("Segoe UI", 9, "bold"),
             fg=C["orig_fg"], bg=C["orig_bg"],
             padx=7, pady=2).pack(side=tk.LEFT, padx=8, pady=4)
    tk.Label(orig_strip, text="reference only — not clickable",
             font=("Segoe UI", 9),
             fg=C["hint"], bg=C["surface"]).pack(side=tk.LEFT)

    orig_canvas = tk.Canvas(left,
                            width=CANVAS_W, height=CANVAS_H,
                            bg=C["canvas_bg"],
                            highlightthickness=0,
                            cursor="arrow")
    orig_canvas.pack()
    widgets["orig_canvas"] = orig_canvas
    draw_placeholder(orig_canvas, "No image loaded")

    # ── Divider ───────────────────────────────────────────────
    tk.Frame(outer, bg=C["border"], width=1).pack(side=tk.LEFT, fill=tk.Y)

    # ── Modified (right) ─────────────────────────────────────
    right = tk.Frame(outer, bg=C["surface"])
    right.pack(side=tk.LEFT)

    mod_strip = tk.Frame(right, bg=C["surface"],
                         highlightbackground=C["border"],
                         highlightthickness=1)
    mod_strip.pack(fill=tk.X)
    tk.Label(mod_strip, text="Modified",
             font=("Segoe UI", 9, "bold"),
             fg=C["mod_fg"], bg=C["mod_bg"],
             padx=7, pady=2).pack(side=tk.LEFT, padx=8, pady=4)
    tk.Label(mod_strip, text="click here to find differences",
             font=("Segoe UI", 9),
             fg=C["hint"], bg=C["surface"]).pack(side=tk.LEFT)

    mod_canvas = tk.Canvas(right,
                           width=CANVAS_W, height=CANVAS_H,
                           bg=C["canvas_bg"],
                           highlightthickness=0,
                           cursor="arrow")
    mod_canvas.pack()
    widgets["mod_canvas"] = mod_canvas
    draw_placeholder(mod_canvas, "No image loaded")


def build_statusbar(root):
    bar = tk.Frame(root, bg=C["surface"], padx=12, pady=6)
    bar.pack(fill=tk.X)

    dot = tk.Label(bar, text="●", font=("Segoe UI", 8),
                   fg=C["dot_warn"], bg=C["surface"])
    dot.pack(side=tk.LEFT, padx=(0, 6))
    widgets["dot"] = dot

    lbl = tk.Label(bar, text="Load an image to start playing.",
                   font=("Segoe UI", 9), fg=C["muted"], bg=C["surface"])
    lbl.pack(side=tk.LEFT)
    widgets["status_lbl"] = lbl


def build_ui():
    root = tk.Tk()
    root.title("Spot the Difference")
    root.resizable(False, False)
    root.configure(bg=C["bg"])

    build_toolbar(root)
    build_separator(root)
    build_statsbar(root)
    build_separator(root)
    build_canvases(root)
    build_separator(root)
    build_statusbar(root)

    return root


# ──────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = build_ui()
    refresh_state()
    root.mainloop()
