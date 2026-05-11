import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import os

# COLOR LIST  ( color pallete created by  the help of LLM )

Color_list = {
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

# Widget references
widgets = {}

# Tkinter StringVars — populated in build_ui()
sv = {}

# Define constants
CANVAS_W    = 560
CANVAS_H    = 380
MAX_MIS     = 3
TOTAL_DIFFS = 5

# Define State variables
state = {
    "game":        "no_image",   # "no_image" | "playing" | "game_over" | "victory"
    "remaining":   TOTAL_DIFFS,
    "mistakes":    0,
    "found":       0,
    "total_mis":   0,
    "demo_toggle": 0,
}

# ___________FUNCTIONS_____________________


def draw_placeholder(canvas, text):
    cx, cy = CANVAS_W // 2, CANVAS_H // 2
    canvas.create_rectangle(cx - 60, cy - 45, cx + 60, cy + 45,
                             outline="#555", width=1)
    canvas.create_line(cx - 60, cy - 45, cx + 60, cy + 45, fill="#555", width=1)
    canvas.create_line(cx + 60, cy - 45, cx - 60, cy + 45, fill="#555", width=1)
    canvas.create_text(cx, cy + 65, text=text, fill="#666",
                       font=("Segoe UI", 10))


def on_load():
    path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"),
                   ("All files", "*.*")],
    )
    if not path:
        return

    sv["filename"].set(os.path.basename(path))
    widgets["button_load"].config(text="⊞  Load image")  # Fix: was "btn_load"

    # Reset per-image state
    state["remaining"]   = TOTAL_DIFFS
    state["mistakes"]    = 0
    state["found"]       = 0
    state["demo_toggle"] = 0
    state["game"]        = "playing"

    widgets["orig_canvas"].delete("all")
    widgets["mod_canvas"].delete("all")


def on_reveal():
    if state["game"] != "playing":
        return
    answer = messagebox.askyesno(
        "Reveal",
        "Reveal all unfound differences?\nYou will need to load a new image.",
    )
    if not answer:
        return


# ______________GUI____________________

def build_canvases(window):
    outer = Frame(window, bg=Color_list["border"])
    outer.pack(fill=BOTH, expand=TRUE)

    # LEFT FRAME
    left_frame = Frame(outer, bg=Color_list["surface"], padx=10, pady=10)
    left_frame.pack(side=LEFT)

    orig_strip = Frame(left_frame, bg=Color_list["surface"],
                       highlightbackground=Color_list["border"],
                       highlightthickness=1)
    orig_strip.pack(fill=X)

    orginal_lable = Label(orig_strip, text="Original",
                          bg=Color_list["orig_bg"],
                          fg=Color_list["orig_fg"],
                          font=("Segoe UI", 9, "bold"),
                          padx=7, pady=2)
    orginal_lable.pack(side=LEFT, padx=8, pady=4)

    orig_canvas = Canvas(left_frame,
                         width=CANVAS_W, height=CANVAS_H,
                         bg=Color_list["canvas_bg"],
                         highlightthickness=0,
                         cursor="arrow")
    orig_canvas.pack()
    widgets["orig_canvas"] = orig_canvas
    draw_placeholder(orig_canvas, "No image loaded")

    # Divider
    border_frame = Frame(outer, bg=Color_list["border"], width=1)
    border_frame.pack(side=LEFT, fill=Y)

    # RIGHT FRAME
    right_mod = Frame(outer, bg=Color_list["surface"])
    right_mod.pack(side=LEFT)

    mod_strip = Frame(right_mod, bg=Color_list["surface"],
                      highlightbackground=Color_list["border"],
                      highlightthickness=1)
    mod_strip.pack(fill=X)

    mod_lable = Label(mod_strip, text="Modified",
                      font=("Segoe UI", 9, "bold"),
                      fg=Color_list["mod_fg"], bg=Color_list["mod_bg"]
                     )
    mod_lable.pack(side=LEFT, padx=8, pady=4)

    clicks_lable = Label(mod_strip, text="click here to find differences",
                         font=("Segoe UI", 9),
                         fg=Color_list["hint"], bg=Color_list["surface"])
    clicks_lable.pack(side=LEFT)

    mod_canvas = Canvas(right_mod,
                        width=CANVAS_W, height=CANVAS_H,
                        bg=Color_list["canvas_bg"],
                        highlightthickness=0,
                        cursor="arrow")
    mod_canvas.pack()
    widgets["mod_canvas"] = mod_canvas
    draw_placeholder(mod_canvas, "No image loaded")


def build_separator(window):
    seperator = Frame(window, bg=Color_list["border"], height=1)
    seperator.pack(fill=X)


def build_toolbar(window):
    bar = Frame(window, bg=Color_list["surface"], pady=6, padx=10)
    bar.pack(fill=X)

    button_load = Button(bar, text="Load Images", bg=Color_list["blue"], fg="white",
                         font=("Segoe UI", 10, "bold"), padx=10, pady=4,
                         cursor="hand2",
                         command=on_load,
                         relief=FLAT,
                         activebackground=Color_list["bg"])
    button_load.pack(side=LEFT, padx=(0, 6))
    button_load.config(highlightbackground=Color_list["border"],
                       highlightcolor=Color_list["border"],
                       highlightthickness=1)
    widgets["button_load"] = button_load

    btn_reveal = Button(bar, text="Reveal all",
                        font=("Segoe UI", 10),
                        fg=Color_list["teal"], bg=Color_list["surface"],
                        activebackground=Color_list["teal_bg"],
                        relief=FLAT, bd=0,
                        padx=10, pady=4,
                        cursor="hand2",
                        command=on_reveal)
    btn_reveal.pack(side=LEFT)
    btn_reveal.config(highlightbackground=Color_list["teal_border"],
                      highlightcolor=Color_list["teal_border"],
                      highlightthickness=1)
    widgets["btn_reveal"] = btn_reveal

    sv["filename"] = StringVar(value="—")
    Label(bar, textvariable=sv["filename"],
          font=("Segoe UI", 9), fg=Color_list["hint"],
          bg=Color_list["surface"]).pack(side=RIGHT, padx=4)

    banner = Label(bar, text="", font=("Segoe UI", 9), pady=3, padx=10)
    widgets["banner"] = banner


def build_statsbar(window):   
    stats_bar = Frame(window, bg=Color_list["surface"], pady=6, padx=10)
    stats_bar.pack(fill=X)

    def sep():
        v_seperator = Frame(stats_bar, bg=Color_list["border"], width=1)
        v_seperator.pack(side=LEFT, fill=Y, padx=6)

    cells = [
        ("Remaining", "remaining", Color_list["blue"]),   
        ("Mistakes",  "mistakes",  Color_list["red"]),    
        ("Found",     "found",     Color_list["green"]),  
    ]

    sv["remaining"] = tk.StringVar(value=str(TOTAL_DIFFS))
    sv["mistakes"]  = tk.StringVar(value=f"0 / {MAX_MIS}")
    sv["found"]     = tk.StringVar(value=f"0 / {TOTAL_DIFFS}")
    sv["total_mis"] = tk.StringVar(value="0")

    for label, key, color in cells:
        f = Frame(stats_bar, bg=Color_list["surface"], padx=14, pady=6)  
        f.pack(side=LEFT)
        Label(f, text=label, font=("Segoe UI", 9),
              fg=Color_list["muted"], bg=Color_list["surface"]).pack(side=LEFT, padx=(0, 5))
        Label(f, textvariable=sv[key],
              font=("Segoe UI", 13, "bold"),
              fg=color, bg=Color_list["surface"]).pack(side=LEFT)
        sep()

    f = Frame(stats_bar, bg=Color_list["surface"], padx=14, pady=6)  
    f.pack(side=RIGHT)
    Label(f, text="Total mistakes", font=("Segoe UI", 9),
          fg=Color_list["muted"], bg=Color_list["surface"]).pack(side=LEFT, padx=(0, 5))
    Label(f, textvariable=sv["total_mis"],
          font=("Segoe UI", 13, "bold"),
          fg=Color_list["text"], bg=Color_list["surface"]).pack(side=LEFT)

def build_statusbar(window):
    status_bar = Frame(window, bg=Color_list["surface"], pady=4, padx=10)
    status_bar.pack(fill=X, side=BOTTOM)
    
    ready_label = Label(status_bar, text="Ready", font=("Segoe UI", 9),
          fg=Color_list["hint"], bg=Color_list["surface"])
    ready_label.pack(side=LEFT)
    widgets["status_bar"] = ready_label


def build_ui():
    window = tk.Tk()
    window.title("Spot The Difference Game")
    window.resizable(False, False)
    window.configure(bg=Color_list["bg"])

    build_toolbar(window)
    build_separator(window)
    build_statsbar(window)
    build_separator(window)
    build_canvases(window)
    build_separator(window)
    build_statusbar(window)

    return window


# ___________Backend interface works_________

#  Stats helpers

def sync_stats():
    sv["remaining"].set(str(state["remaining"]))
    sv["mistakes"].set(f"{state['mistakes']} / {MAX_MIS}")
    sv["found"].set(f"{state['found']} / {TOTAL_DIFFS}")
    sv["total_mis"].set(str(state["total_mis"]))






















if __name__ == "__main__":
    window = build_ui()
    window.mainloop()

