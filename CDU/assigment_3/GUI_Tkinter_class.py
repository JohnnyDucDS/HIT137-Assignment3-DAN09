import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import os


class SpotTheDifferenceApp:

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
        "dot_err":     "#CE2C2C",
    }

    CANVAS_W    = 560
    CANVAS_H    = 380
    MAX_MIS     = 3
    TOTAL_DIFFS = 5

    def __init__(self):
        self.widgets = {}
        self.sv = {}
        self.state = {
            "game":        "no_image",   # "no_image" | "playing" | "game_over" | "victory"
            "remaining":   self.TOTAL_DIFFS,
            "mistakes":    0,
            "found":       0,
            "total_mis":   0,
            "demo_toggle": 0,    # REMOVE THIS DEMO_TOGGLE AFTER THE MEREGE AND REMOVE DEMO CODE BELOW AS WELL
        }
        self.window = self.build_ui()
        self.window.mainloop()

    # ______________GUI____________________

    def build_canvases(self, window):
        outer = Frame(window, bg=self.Color_list["border"])
        outer.pack(fill=BOTH, expand=TRUE)

        # LEFT FRAME
        left_frame = Frame(outer, bg=self.Color_list["surface"], padx=10, pady=10)
        left_frame.pack(side=LEFT)

        orig_strip = Frame(left_frame, bg=self.Color_list["surface"],
                           highlightbackground=self.Color_list["border"],
                           highlightthickness=1)
        orig_strip.pack(fill=X)

        orginal_lable = Label(orig_strip, text="Original",
                              bg=self.Color_list["orig_bg"],
                              fg=self.Color_list["orig_fg"],
                              font=("Segoe UI", 9, "bold"),
                              padx=7, pady=2)
        orginal_lable.pack(side=LEFT, padx=8, pady=4)

        orig_canvas = Canvas(left_frame,
                             width=self.CANVAS_W, height=self.CANVAS_H,
                             bg=self.Color_list["canvas_bg"],
                             highlightthickness=0,
                             cursor="arrow")
        orig_canvas.pack()

        self.widgets["orig_canvas"] = orig_canvas
        self.draw_placeholder(orig_canvas, "No image loaded")

        # Divider
        border_frame = Frame(outer, bg=self.Color_list["border"], width=1)
        border_frame.pack(side=LEFT, fill=Y)

        # RIGHT FRAME
        right_mod = Frame(outer, bg=self.Color_list["surface"])
        right_mod.pack(side=LEFT)

        mod_strip = Frame(right_mod, bg=self.Color_list["surface"],
                          highlightbackground=self.Color_list["border"],
                          highlightthickness=1)
        mod_strip.pack(fill=X)

        mod_lable = Label(mod_strip, text="Modified",
                          font=("Segoe UI", 9, "bold"),
                          fg=self.Color_list["mod_fg"], bg=self.Color_list["mod_bg"])
        mod_lable.pack(side=LEFT, padx=8, pady=4)

        clicks_lable = Label(mod_strip, text="click here to find differences",
                             font=("Segoe UI", 9),
                             fg=self.Color_list["hint"], bg=self.Color_list["surface"])
        clicks_lable.pack(side=LEFT)

        mod_canvas = Canvas(right_mod,
                            width=self.CANVAS_W, height=self.CANVAS_H,
                            bg=self.Color_list["canvas_bg"],
                            highlightthickness=0,
                            cursor="arrow")
        mod_canvas.pack()
        self.widgets["mod_canvas"] = mod_canvas
        self.draw_placeholder(mod_canvas, "No image loaded")

    def build_separator(self, window):
        seperator = Frame(window, bg=self.Color_list["border"], height=1)
        seperator.pack(fill=X)

    def build_toolbar(self, window):
        bar = Frame(window, bg=self.Color_list["surface"], pady=6, padx=10)
        bar.pack(fill=X)

        button_load = Button(bar, text="Load Images", bg=self.Color_list["blue"], fg="white",
                             font=("Segoe UI", 10, "bold"), padx=10, pady=4,
                             cursor="hand2",
                             command=self.on_load,
                             relief=FLAT,
                             activebackground=self.Color_list["bg"])
        button_load.pack(side=LEFT, padx=(0, 6))
        button_load.config(highlightbackground=self.Color_list["border"],
                           highlightcolor=self.Color_list["border"],
                           highlightthickness=1)
        self.widgets["button_load"] = button_load

        btn_reveal = Button(bar, text="Reveal all",
                            font=("Segoe UI", 10),
                            fg=self.Color_list["teal"], bg=self.Color_list["surface"],
                            activebackground=self.Color_list["teal_bg"],
                            relief=FLAT, bd=0,
                            padx=10, pady=4,
                            cursor="hand2",
                            command=self.on_reveal)
        btn_reveal.pack(side=LEFT)
        btn_reveal.config(highlightbackground=self.Color_list["teal_border"],
                          highlightcolor=self.Color_list["teal_border"],
                          highlightthickness=1)
        self.widgets["btn_reveal"] = btn_reveal

        self.sv["filename"] = StringVar(value="—")
        Label(bar, textvariable=self.sv["filename"],
              font=("Segoe UI", 9), fg=self.Color_list["hint"],
              bg=self.Color_list["surface"]).pack(side=RIGHT, padx=4)

        banner = Label(bar, text="", font=("Segoe UI", 9), pady=3, padx=10)
        self.widgets["banner"] = banner

    def build_statsbar(self, window):
        stats_bar = Frame(window, bg=self.Color_list["surface"], pady=6, padx=10)
        stats_bar.pack(fill=X)

        def sep():
            v_seperator = Frame(stats_bar, bg=self.Color_list["border"], width=1)
            v_seperator.pack(side=LEFT, fill=Y, padx=6)

        cells = [
            ("Remaining", "remaining", self.Color_list["blue"]),
            ("Mistakes",  "mistakes",  self.Color_list["red"]),
            ("Found",     "found",     self.Color_list["green"]),
        ]

        self.sv["remaining"] = StringVar(value=str(self.TOTAL_DIFFS))
        self.sv["mistakes"]  = StringVar(value=f"0 / {self.MAX_MIS}")
        self.sv["found"]     = StringVar(value="0")
        self.sv["total_mis"] = StringVar(value="0")

        for label, key, color in cells:
            f = Frame(stats_bar, bg=self.Color_list["surface"], padx=14, pady=6)
            f.pack(side=LEFT)
            Label(f, text=label, font=("Segoe UI", 9),
                  fg=self.Color_list["muted"], bg=self.Color_list["surface"]).pack(side=LEFT, padx=(0, 5))
            Label(f, textvariable=self.sv[key],
                  font=("Segoe UI", 13, "bold"),
                  fg=color, bg=self.Color_list["surface"]).pack(side=LEFT)
            sep()

        f = Frame(stats_bar, bg=self.Color_list["surface"], padx=14, pady=6)
        f.pack(side=RIGHT)

        total_mistake = Label(f, text="Total mistakes", font=("Segoe UI", 9),
              fg=self.Color_list["muted"], bg=self.Color_list["surface"])
        total_mistake.pack(side=LEFT, padx=(0, 5))

        total_miss = Label(f, textvariable=self.sv["total_mis"],
              font=("Segoe UI", 13, "bold"),
              fg=self.Color_list["text"], bg=self.Color_list["surface"])
        total_miss.pack(side=LEFT)

    def build_statusbar(self, window):
        status_bar = Frame(window, bg=self.Color_list["surface"], pady=4, padx=10)
        status_bar.pack(fill=X, side=BOTTOM)

        dot = Label(status_bar, text="●", font=("Segoe UI", 9),
                    fg=self.Color_list["dot_warn"], bg=self.Color_list["surface"])
        dot.pack(side=LEFT, padx=(0, 4))
        self.widgets["dot"] = dot

        status_lbl = Label(status_bar, text="Load an image to start playing.",
                           font=("Segoe UI", 9),
                           fg=self.Color_list["hint"], bg=self.Color_list["surface"])
        status_lbl.pack(side=LEFT)
        self.widgets["status_lbl"] = status_lbl

    def build_ui(self):
        window = tk.Tk()
        window.title("Spot The Difference Game")
        window.resizable(False, False)
        window.configure(bg=self.Color_list["bg"])

        self.build_toolbar(window)
        self.build_separator(window)
        self.build_statsbar(window)
        self.build_separator(window)
        self.build_canvases(window)
        self.build_separator(window)
        self.build_statusbar(window)

        return window

    # ___________Backend interface works_________

    def sync_stats(self):
        self.sv["remaining"].set(str(self.state["remaining"]))
        self.sv["mistakes"].set(f"{self.state['mistakes']} / {self.MAX_MIS}")
        self.sv["found"].set(str(self.state["found"]))
        self.sv["total_mis"].set(str(self.state["total_mis"]))

    def refresh_state(self):
        """Update every widget to match the current game state."""
        g = self.state["game"]

        self.widgets["button_load"].config(state=NORMAL, cursor="hand2")

        if g == "no_image":
            self.widgets["btn_reveal"].config(state=DISABLED, cursor="arrow",
                                              fg=self.Color_list["hint"])
            self.set_status("Load an image to start playing.", self.Color_list["dot_warn"])
            self.hide_banner()

        elif g == "playing":
            self.widgets["btn_reveal"].config(state=NORMAL, cursor="hand2",
                                              fg=self.Color_list["teal"])
            self.widgets["mod_canvas"].config(cursor="crosshair")
            self.widgets["mod_canvas"].bind("<Button-1>", self.on_canvas_click)
            self.set_status("Click on the right image to find differences.", self.Color_list["dot_ok"])
            self.hide_banner()

        elif g == "game_over":
            self.widgets["btn_reveal"].config(state=DISABLED, cursor="arrow",
                                              fg=self.Color_list["hint"])
            self.widgets["mod_canvas"].config(cursor="arrow")
            self.widgets["mod_canvas"].unbind("<Button-1>")
            self.set_status("Maximum mistakes reached — load a new image to continue.",
                            self.Color_list["dot_err"])
            self.show_banner("  ⚠  Too many mistakes — load a new image",
                             bg=self.Color_list["red_bg"], fg=self.Color_list["red_label"],
                             border=self.Color_list["red"])
            self.draw_gameover_overlay()

        elif g == "victory":
            self.widgets["btn_reveal"].config(state=DISABLED, cursor="arrow",
                                              fg=self.Color_list["hint"])
            self.widgets["button_load"].config(text="Load next image")
            self.widgets["mod_canvas"].config(cursor="arrow")
            self.widgets["mod_canvas"].unbind("<Button-1>")
            self.set_status(
                "Congratulations — all 5 found! Load a new image to keep playing.",
                self.Color_list["dot_ok"])
            self.show_banner("  ✓  All 5 found! Load a new image to continue",
                             bg=self.Color_list["green_bg"], fg=self.Color_list["green_label"],
                             border="#97C459")

        self.sync_stats()

    def set_status(self, text, dot_color):
        self.widgets["dot"].config(fg=dot_color)
        self.widgets["status_lbl"].config(text=text)

    def show_banner(self, text, bg, fg, border):
        self.widgets["banner"].config(text=text, bg=bg, fg=fg,
                                      highlightbackground=border,
                                      highlightthickness=1)
        self.widgets["banner"].pack(side=tk.RIGHT, padx=8)

    def hide_banner(self):
        self.widgets["banner"].pack_forget()

    # ________ Canvas drawing _______

    def draw_found_circle(self, x, y, r=28):
        # Red circle on both canvases at the same position
        for canvas in (self.widgets["orig_canvas"], self.widgets["mod_canvas"]):
            canvas.create_oval(x - r, y - r, x + r, y + r,
                               outline="#e53935", width=3, tags="marker")

    def draw_reveal_circle(self, x, y, r=28):
        # Blue circle on both canvases
        for canvas in (self.widgets["orig_canvas"], self.widgets["mod_canvas"]):
            canvas.create_oval(x - r, y - r, x + r, y + r,
                               outline="#1565C0", width=3, tags="marker")

    def draw_wrong_click(self, x, y):
        # Small red ✕ on the modified canvas
        s = 7
        self.widgets["mod_canvas"].create_line(x - s, y - s, x + s, y + s,
                                               fill="#e53935", width=2, tags="marker")
        self.widgets["mod_canvas"].create_line(x + s, y - s, x - s, y + s,
                                               fill="#e53935", width=2, tags="marker")

    def draw_gameover_overlay(self):
        c = self.widgets["mod_canvas"]
        cx, cy = self.CANVAS_W // 2, self.CANVAS_H // 2
        c.create_rectangle(0, 0, self.CANVAS_W, self.CANVAS_H,
                           fill="#A32D2D", stipple="gray25",
                           outline="", tags="overlay")
        c.create_rectangle(cx - 110, cy - 18, cx + 110, cy + 18,
                           fill="#A32D2D", outline="", tags="overlay")
        c.create_text(cx, cy,
                      text="Game over — 3 mistakes",
                      fill="#FCEBEB", font=("Segoe UI", 11, "bold"),
                      tags="overlay")

    def draw_placeholder(self, canvas, text):
        cx, cy = self.CANVAS_W // 2, self.CANVAS_H // 2
        canvas.create_rectangle(cx - 60, cy - 45, cx + 60, cy + 45,
                                 outline="#555", width=1)
        canvas.create_line(cx - 60, cy - 45, cx + 60, cy + 45, fill="#555", width=1)
        canvas.create_line(cx + 60, cy - 45, cx - 60, cy + 45, fill="#555", width=1)
        canvas.create_text(cx, cy + 65, text=text, fill="#666",
                           font=("Segoe UI", 10))

    # ______Event handlers________

    def on_load(self):
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"),
                       ("All files", "*.*")],
        )
        if not path:
            return

        self.sv["filename"].set(os.path.basename(path))
        self.widgets["button_load"].config(text="⊞  Load image")

        # Reset per-image state
        self.state["remaining"]   = self.TOTAL_DIFFS
        self.state["mistakes"]    = 0
        self.state["demo_toggle"] = 0
        self.state["game"]        = "playing"

        self.widgets["orig_canvas"].delete("all")
        self.widgets["mod_canvas"].delete("all")

        self.refresh_state()

        # Test (remove when compile with imageproceesors)
        self.widgets["orig_canvas"].create_text(
            self.CANVAS_W // 2, self.CANVAS_H // 2,
            text=f"Original image\n{os.path.basename(path)}",
            fill="#aaa", font=("Segoe UI", 11), justify=tk.CENTER)
        self.widgets["mod_canvas"].create_text(
            self.CANVAS_W // 2, self.CANVAS_H // 2,
            text="Modified image\n(5 hidden differences)",
            fill="#aaa", font=("Segoe UI", 11), justify=tk.CENTER)

        #----remove the test, uncomment the code below and replace
        # the placeholder with real ImageProcessor
        '''
            # replace these two lines with real ImageProcessor calls
         image_processor.load(path)
         orig_photo = image_processor.to_tk_image(image_processor.original)
         mod_photo  = image_processor.to_tk_image(image_processor.modified)
         self.widgets["orig_canvas"].create_image(self.CANVAS_W//2, self.CANVAS_H//2,
                                             anchor=tk.CENTER, image=orig_photo)
         self.widgets["mod_canvas"].create_image(self.CANVAS_W//2, self.CANVAS_H//2,
                                            anchor=tk.CENTER, image=mod_photo)
        '''

    def on_reveal(self):
        if self.state["game"] != "playing":
            return
        answer = messagebox.askyesno(
            "Reveal",
            "Reveal all unfound differences?\nYou will need to load a new image.",
        )
        if not answer:
            return

        # ── Hook: replace with real game logic ────────────────────────────
        # for diff in game_state.unfound():
        #     self.draw_reveal_circle(diff.cx, diff.cy, diff.radius())
        # ─────────────────────────────────────────────────────────────────

        # DEMO
        for cx, cy in [(140, 130), (280, 200), (430, 110)]:
            self.draw_reveal_circle(cx, cy, 30)

        self.state["game"] = "game_over"
        self.refresh_state()

    def on_canvas_click(self, event):
        if self.state["game"] != "playing":
            return

        x, y = event.x, event.y

        # ── Hook: replace with real game logic ────────────────────────────
        # diff = game_state.check_click(x, y)
        # if diff:
        #     self.draw_found_circle(diff.cx, diff.cy, diff.radius())
        #     self.state["found"]     += 1
        #     self.state["remaining"] -= 1
        #     self.sync_stats()
        #     if self.state["remaining"] == 0:
        #         self.state["game"] = "victory"
        #         self.refresh_state()
        #         messagebox.showinfo("You win!", "All 5 differences found!")
        # else:
        #     self.draw_wrong_click(x, y)
        #     self.state["mistakes"]  += 1
        #     self.state["total_mis"] += 1
        #     self.sync_stats()
        #     if self.state["mistakes"] >= self.MAX_MIS:
        #         self.state["game"] = "game_over"
        #         self.refresh_state()

        # DEMO: alternate correct / wrong for testing
        self.state["demo_toggle"] += 1
        if self.state["demo_toggle"] % 2 == 1:
            self.draw_found_circle(x, y)
            self.state["found"]     += 1
            self.state["remaining"] -= 1
            self.sync_stats()
            if self.state["remaining"] <= 0:
                self.state["game"] = "victory"
                self.refresh_state()
                messagebox.showinfo("Congratulations!",
                                    "You found all 5 differences!\n"
                                    "Load a new image to continue.")
        else:
            self.draw_wrong_click(x, y)
            self.state["mistakes"]  += 1
            self.state["total_mis"] += 1
            self.sync_stats()
            if self.state["mistakes"] >= self.MAX_MIS:
                self.state["game"] = "game_over"
                self.refresh_state()


if __name__ == "__main__":
    SpotTheDifferenceApp()
