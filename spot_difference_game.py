
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import os
import random
import cv2
import numpy as np
from PIL import Image, ImageTk


# Difference Class

class Difference:
    def __init__(self, x, y, width, height, alteration_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alteration_type = alteration_type
        self.found = False

    def contains_point(self, click_x, click_y):     # click inside the box
        return (
            self.x <= click_x <= self.x + self.width
            and self.y <= click_y <= self.y + self.height
        )  

    def overlaps_with(self, other):
        return not (
            self.x + self.width < other.x or
            other.x + other.width < self.x or
            self.y + self.height < other.y or
            other.y + other.height < self.y
        )   # not not overlap

    def center(self):
        return self.x + self.width // 2, self.y + self.height // 2

    def radius(self):
        return max(self.width, self.height) // 2 + 8


# ImageProcessor Class

class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.modified_image = None
        self.differences = []

    def load_image(self, file_path, target_width=560, target_height=380):
        pil_image = Image.open(file_path).convert("RGB") #forces every images into 3 channels
 
        image = cv2.cvtColor(
            np.array(pil_image),
            cv2.COLOR_RGB2BGR
        )

        image = cv2.resize(image, (target_width, target_height))

        self.original_image = image
        self.modified_image = image.copy()
        self.differences = []

    def create_modified_image(self):
        for _ in range(5):
            difference = self.generate_non_overlapping_difference()
            self.differences.append(difference)
            self.apply_alteration(difference)

    def generate_non_overlapping_difference(self):
        image_height, image_width = self.original_image.shape[:2]

        max_attempts = 100

        for _ in range(max_attempts):
            width = random.randint(10, 20)
            height = random.randint(10, 20)

            x = random.randint(0, image_width - width)
            y = random.randint(0, image_height - height)

            alteration_type = random.choice([
                "colour_shift",
                "blur",
                "brightness",
                "rectangle"
            ])

            new_difference = Difference(x, y, width, height, alteration_type)

            overlap = False
            for existing_difference in self.differences:
                if new_difference.overlaps_with(existing_difference):
                    overlap = True
                    break

            if not overlap:
                return new_difference

        raise RuntimeError("Could not generate non-overlapping difference.")

    def get_region(self, difference):
        return self.modified_image[
            difference.y:difference.y + difference.height,
            difference.x:difference.x + difference.width
        ]

    def apply_alteration(self, difference):
        if difference.alteration_type == "colour_shift":
            self.apply_colour_shift(difference)

        elif difference.alteration_type == "blur":
            self.apply_blur(difference)

        elif difference.alteration_type == "brightness":
            self.apply_brightness_change(difference)

        elif difference.alteration_type == "rectangle":
            self.apply_rectangle(difference)

    def apply_colour_shift(self, difference):
        region = self.get_region(difference)

        # 0 = Blue, 1 = Green, 2 = Red
        channel = random.randint(0, 2)
        shift_amount = random.randint(-70, 70)  # apply darker or brighter

        region[:, :, channel] = cv2.add(
            region[:, :, channel],
            shift_amount
        )

    def apply_blur(self, difference):
        region = self.get_region(difference)

        blurred_region = cv2.GaussianBlur(region, (15, 15), 0)  # img[i, j] = (img[i, j-1] + img[i, j] + img[i, j+1]) // 3 

        self.modified_image[
            difference.y:difference.y + difference.height,
            difference.x:difference.x + difference.width
        ] = blurred_region

    def apply_brightness_change(self, difference):
        region = self.get_region(difference)

        brighter_region = cv2.convertScaleAbs(
            region,
            alpha=1.0,
            beta=random.randint(35, 65)
        )   # new_pixel = abs(alpha * pixel + beta)

        self.modified_image[
            difference.y:difference.y + difference.height,
            difference.x:difference.x + difference.width
        ] = brighter_region

    def apply_rectangle(self, difference):
        x1 = difference.x
        y1 = difference.y
        x2 = difference.x + difference.width - 5
        y2 = difference.y + difference.height - 5   # this alteration easier to spot than the other with same region

        region = self.original_image[y1:y2, x1:x2]

        # Get average background colour in this area
        avg_color = region.mean(axis=(0, 1))  # BGR average on columns rows

        # small random change so it is visible but not too obvious
        subtle_color = []
        for value in avg_color:
            new_value = int(value + random.randint(-25, 25))
            new_value = max(0, min(255, new_value)) # keep it in colour range
            subtle_color.append(new_value)

        color = tuple(subtle_color)

        cv2.rectangle(
            self.modified_image,
            (x1, y1),
            (x2, y2),
            color,
            thickness=2
        )
        
    def convert_to_tk_image(self, cv_image):
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        return ImageTk.PhotoImage(pil_image)


# GameManager Class

class GameManager:
    def __init__(self):
        # handles loading image and generating differences
        self.image_processor = ImageProcessor()

        # Game settings
        self.total_differences = 5
        self.max_mistakes = 3

        # Track current game progress
        self.remaining = 5     # differences left to find
        self.found = 0         # how many already found
        self.mistakes = 0      # mistakes in current round

        # Keep track of mistakes across multiple rounds
        self.total_mistakes = 0

        # Game state:
        # no_image → before loading image
        # playing → game running
        # victory → all differences found
        # game_over → too many mistakes
        self.game_state = "no_image"

    def start_new_game(self, file_path, width, height):
        """
        load image
        generate 5 differences
        reset score and mistakes
        """
        # send image to ImageProcessor
        self.image_processor.load_image(
            file_path,
            width,
            height
        )

        # Create modified image with hidden differences
        self.image_processor.create_modified_image()
        # Reset game stats
        self.remaining = self.total_differences
        self.found = 0
        self.mistakes = 0

        self.game_state = "playing"

    def check_click(self, x, y):
        """
        Check whether player's click is correct.

        If player clicks inside a hidden difference:
        → mark it as found

        Otherwise:
        → count as a mistake
        """

        # ignore clicks if game not active
        if self.game_state != "playing":
            return None

        # loop through all generated differences
        for difference in self.image_processor.differences:

            # only check differences not found yet
            if (
                not difference.found
                and difference.contains_point(x, y)
            ):

                # mark difference as found
                difference.found = True

                # score
                self.found += 1
                self.remaining -= 1

                # all differences found
                if self.remaining == 0:
                    self.game_state = "victory"

                # Return found difference
                # GUI uses this to draw red circle
                return difference

        # If no difference matched → wrong click
        self.mistakes += 1
        self.total_mistakes += 1

        # Lose condition:
        # too many mistakes
        if self.mistakes >= self.max_mistakes:
            self.game_state = "game_over"

        return None

    def get_unfound_differences(self):
        """
        Return all differences that player
        has not found yet.
        Used for the Reveal button.
        """

        return [
            difference
            for difference in self.image_processor.differences
            if not difference.found
        ]

# GUI Class

class SpotTheDifferenceApp:

    # colour palette used across the whole UI
    Color_list = {
        "bg": "#f5f5f3",
        "surface": "#ffffff",
        "canvas_bg": "#2a2a2a",
        "border": "#e0ddd8",
        "text": "#1a1a1a",
        "muted": "#6b7280",
        "hint": "#9ca3af",
        "blue": "#185FA5",
        "red": "#A32D2D",
        "red_bg": "#fcebeb",
        "red_label": "#791F1F",
        "green": "#3B6D11",
        "green_bg": "#eaf3de",
        "green_label": "#27500A",
        "teal": "#0F6E56",
        "teal_bg": "#E1F5EE",
        "teal_border": "#5DCAA5",
        "orig_bg": "#E1F5EE",
        "orig_fg": "#085041",
        "mod_bg": "#E6F1FB",
        "mod_fg": "#0C447C",
        "dot_ok": "#28c840",
        "dot_warn": "#febc2e",
        "dot_err": "#CE2C2C",
    }

    CANVAS_W = 560
    CANVAS_H = 380
    MAX_MIS = 3
    TOTAL_DIFFS = 5

    def __init__(self):
        self.widgets = {}  # central dict so any method can reach any widget
        self.sv = {}       # StringVar dict for live stat labels

        self.game_manager = GameManager()
        self._ended_by_reveal = False

        # keep photo refs here — if they go out of scope tkinter drops the image
        self.original_photo = None
        self.modified_photo = None

        self.window = self.build_ui()
        self.refresh_state()
        self.window.mainloop()

    # ================= GUI BUILDING =================

    # create the main window and assemble all sections top to bottom
    def build_ui(self):
        window = tk.Tk()
        window.title("Spot The Difference Game")
        window.resizable(False, False)
        window.configure(bg=self.Color_list["bg"])

        # stacked top to bottom
        self.build_toolbar(window)
        self.build_separator(window)
        self.build_statsbar(window)
        self.build_separator(window)
        self.build_canvases(window)
        self.build_separator(window)
        self.build_statusbar(window)

        return window

    # thin 1px horizontal divider between sections
    def build_separator(self, window):
        # thin horizontal line between sections
        separator = Frame(window, bg=self.Color_list["border"], height=1)
        separator.pack(fill=X)

    # top bar with Load / Reveal buttons and filename label
    def build_toolbar(self, window):
        bar = Frame(window, bg=self.Color_list["surface"], pady=6, padx=10)
        bar.pack(fill=X)

        button_load = Button(
            bar,
            text="Load Image",
            bg=self.Color_list["blue"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.on_load,
            relief=FLAT
        )
        button_load.pack(side=LEFT, padx=(0, 6))
        self.widgets["button_load"] = button_load

        btn_reveal = Button(
            bar,
            text="Reveal all",
            font=("Segoe UI", 10),
            fg=self.Color_list["teal"],
            bg=self.Color_list["surface"],
            relief=FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.on_reveal
        )
        btn_reveal.pack(side=LEFT)
        self.widgets["btn_reveal"] = btn_reveal

        # filename shown on the right of the toolbar
        self.sv["filename"] = StringVar(value="—")
        Label(
            bar,
            textvariable=self.sv["filename"],
            font=("Segoe UI", 9),
            fg=self.Color_list["hint"],
            bg=self.Color_list["surface"]
        ).pack(side=RIGHT, padx=4)

        # banner for win/loss messages, hidden until needed
        banner = Label(bar, text="", font=("Segoe UI", 9), pady=3, padx=10)
        self.widgets["banner"] = banner

    # row of live counters: remaining, mistakes, found, total mistakes
    def build_statsbar(self, window):
        stats_bar = Frame(window, bg=self.Color_list["surface"], pady=6, padx=10)
        stats_bar.pack(fill=X)

        self.sv["remaining"] = StringVar(value=str(self.TOTAL_DIFFS))
        self.sv["mistakes"] = StringVar(value=f"0 / {self.MAX_MIS}")
        self.sv["found"] = StringVar(value="0")
        self.sv["total_mis"] = StringVar(value="0")

        # three main counters on the left
        cells = [
            ("Remaining", "remaining", self.Color_list["blue"]),
            ("Mistakes", "mistakes", self.Color_list["red"]),
            ("Found", "found", self.Color_list["green"]),
        ]

        for label, key, color in cells:
            frame = Frame(stats_bar, bg=self.Color_list["surface"], padx=14, pady=6)
            frame.pack(side=LEFT)

            Label(
                frame,
                text=label,
                font=("Segoe UI", 9),
                fg=self.Color_list["muted"],
                bg=self.Color_list["surface"]
            ).pack(side=LEFT, padx=(0, 5))

            Label(
                frame,
                textvariable=self.sv[key],
                font=("Segoe UI", 13, "bold"),
                fg=color,
                bg=self.Color_list["surface"]
            ).pack(side=LEFT)

        # total mistakes counter lives on the right
        frame = Frame(stats_bar, bg=self.Color_list["surface"], padx=14, pady=6)
        frame.pack(side=RIGHT)

        Label(
            frame,
            text="Total mistakes",
            font=("Segoe UI", 9),
            fg=self.Color_list["muted"],
            bg=self.Color_list["surface"]
        ).pack(side=LEFT, padx=(0, 5))

        Label(
            frame,
            textvariable=self.sv["total_mis"],
            font=("Segoe UI", 13, "bold"),
            fg=self.Color_list["text"],
            bg=self.Color_list["surface"]
        ).pack(side=LEFT)

    # side-by-side original and modified image canvases
    def build_canvases(self, window):
        outer = Frame(window, bg=self.Color_list["border"])
        outer.pack(fill=BOTH, expand=True)

        # Left — original image (read-only, no click binding)
        left_frame = Frame(outer, bg=self.Color_list["surface"], padx=10, pady=10)
        left_frame.pack(side=LEFT)

        Label(
            left_frame,
            text="Original",
            bg=self.Color_list["orig_bg"],
            fg=self.Color_list["orig_fg"],
            font=("Segoe UI", 9, "bold"),
            padx=7,
            pady=2
        ).pack(anchor=W)

        orig_canvas = Canvas(
            left_frame,
            width=self.CANVAS_W,
            height=self.CANVAS_H,
            bg=self.Color_list["canvas_bg"],
            highlightthickness=0
        )
        orig_canvas.pack()

        self.widgets["orig_canvas"] = orig_canvas
        self.draw_placeholder(orig_canvas, "No image loaded")

        # Right — modified image, player clicks here
        right_frame = Frame(outer, bg=self.Color_list["surface"], padx=10, pady=10)
        right_frame.pack(side=LEFT)

        Label(
            right_frame,
            text="Modified - click here",
            bg=self.Color_list["mod_bg"],
            fg=self.Color_list["mod_fg"],
            font=("Segoe UI", 9, "bold"),
            padx=7,
            pady=2
        ).pack(anchor=W)

        mod_canvas = Canvas(
            right_frame,
            width=self.CANVAS_W,
            height=self.CANVAS_H,
            bg=self.Color_list["canvas_bg"],
            highlightthickness=0,
            cursor="arrow"
        )
        mod_canvas.pack()

        self.widgets["mod_canvas"] = mod_canvas
        self.draw_placeholder(mod_canvas, "No image loaded")

    # bottom bar with a coloured dot and a short status message
    def build_statusbar(self, window):
        status_bar = Frame(window, bg=self.Color_list["surface"], pady=4, padx=10)
        status_bar.pack(fill=X, side=BOTTOM)

        # coloured dot gives a quick visual state at a glance
        dot = Label(
            status_bar,
            text="●",
            font=("Segoe UI", 9),
            fg=self.Color_list["dot_warn"],
            bg=self.Color_list["surface"]
        )
        dot.pack(side=LEFT, padx=(0, 4))
        self.widgets["dot"] = dot

        status_lbl = Label(
            status_bar,
            text="Load an image to start playing.",
            font=("Segoe UI", 9),
            fg=self.Color_list["hint"],
            bg=self.Color_list["surface"]
        )
        status_lbl.pack(side=LEFT)
        self.widgets["status_lbl"] = status_lbl

    # ================= STATE / DISPLAY =================

    # push latest game numbers into the StringVars so labels update automatically
    def sync_stats(self):
        # push latest game numbers into the StringVars
        self.sv["remaining"].set(str(self.game_manager.remaining))
        self.sv["mistakes"].set(f"{self.game_manager.mistakes} / {self.MAX_MIS}")
        self.sv["found"].set(str(self.game_manager.found))
        self.sv["total_mis"].set(str(self.game_manager.total_mistakes))

    # sync the entire UI to match the current game_state
    def refresh_state(self):
        # central place that syncs the whole UI to the current game state
        game_state = self.game_manager.game_state

        if game_state == "no_image":
            self.widgets["btn_reveal"].config(state=DISABLED, cursor="arrow")
            self.set_status("Load an image to start playing.", self.Color_list["dot_warn"])
            self.hide_banner()

        elif game_state == "playing":
            self.widgets["btn_reveal"].config(state=NORMAL, cursor="hand2")
            self.widgets["mod_canvas"].config(cursor="crosshair")
            self.widgets["mod_canvas"].bind("<Button-1>", self.on_canvas_click)
            self.set_status("Click on the right image to find differences.", self.Color_list["dot_ok"])
            self.hide_banner()

        elif game_state == "game_over":
            self.widgets["btn_reveal"].config(state=DISABLED, cursor="arrow")
            self.widgets["mod_canvas"].config(cursor="arrow")
            self.widgets["mod_canvas"].unbind("<Button-1>")  # stop accepting clicks
            self.set_status("Maximum mistakes reached.", self.Color_list["dot_err"])
            self.show_banner(
                "  ⚠ Too many mistakes",
                bg=self.Color_list["red_bg"],
                fg=self.Color_list["red_label"],
                border=self.Color_list["red"]
            )
            self.draw_gameover_overlay()

        elif game_state == "victory":
            self.widgets["btn_reveal"].config(state=DISABLED, cursor="arrow")
            self.widgets["mod_canvas"].config(cursor="arrow")
            self.widgets["mod_canvas"].unbind("<Button-1>")
            self.set_status("Congratulations — all 5 found!", self.Color_list["dot_ok"])
            self.show_banner(
                "  ✓ All 5 found!",
                bg=self.Color_list["green_bg"],
                fg=self.Color_list["green_label"],
                border="#97C459"
            )

        self.sync_stats()

    # update the dot colour and message in the status bar
    def set_status(self, text, dot_color):
        self.widgets["dot"].config(fg=dot_color)
        self.widgets["status_lbl"].config(text=text)

    # show the win/loss banner on the right side of the toolbar
    def show_banner(self, text, bg, fg, border):
        self.widgets["banner"].config(
            text=text,
            bg=bg,
            fg=fg,
            highlightbackground=border,
            highlightthickness=1
        )
        self.widgets["banner"].pack(side=RIGHT, padx=8)

    # remove the banner from layout without destroying it
    def hide_banner(self):
        self.widgets["banner"].pack_forget()

    # render the current original and modified images onto both canvases
    def display_images(self):
        processor = self.game_manager.image_processor

        # convert cv2 images to tkinter-compatible format
        self.original_photo = processor.convert_to_tk_image(processor.original_image)
        self.modified_photo = processor.convert_to_tk_image(processor.modified_image)

        # clear old content then draw fresh
        self.widgets["orig_canvas"].delete("all")
        self.widgets["mod_canvas"].delete("all")

        self.widgets["orig_canvas"].create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.original_photo
        )

        self.widgets["mod_canvas"].create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.modified_photo
        )

    # ================= DRAWING =================

    # draw a box-with-X icon when no image is loaded yet
    def draw_placeholder(self, canvas, text):
        # draws an X inside a box — standard "no image" icon
        cx, cy = self.CANVAS_W // 2, self.CANVAS_H // 2

        canvas.create_rectangle(cx - 60, cy - 45, cx + 60, cy + 45, outline="#555")
        canvas.create_line(cx - 60, cy - 45, cx + 60, cy + 45, fill="#555")
        canvas.create_line(cx + 60, cy - 45, cx - 60, cy + 45, fill="#555")
        canvas.create_text(cx, cy + 65, text=text, fill="#666", font=("Segoe UI", 10))

    # draw a red circle on both canvases to mark a correctly found difference
    def draw_found_circle(self, x, y, r=28):
        # red circle on both canvases to mark a found spot
        for canvas in (self.widgets["orig_canvas"], self.widgets["mod_canvas"]):
            canvas.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                outline="#e53935",
                width=3,
                tags="marker"
            )

    # draw a blue circle on both canvases when a difference is revealed by the button
    def draw_reveal_circle(self, x, y, r=28):
        # blue circle — same shape but different colour for revealed spots
        for canvas in (self.widgets["orig_canvas"], self.widgets["mod_canvas"]):
            canvas.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                outline="#1565C0",
                width=3,
                tags="marker"
            )

    # draw a small red X on the modified canvas where the player missed
    def draw_wrong_click(self, x, y):
        # small red X where the player clicked wrong
        s = 7
        canvas = self.widgets["mod_canvas"]

        canvas.create_line(
            x - s,
            y - s,
            x + s,
            y + s,
            fill="#e53935",
            width=2,
            tags="marker"
        )

        canvas.create_line(
            x + s,
            y - s,
            x - s,
            y + s,
            fill="#e53935",
            width=2,
            tags="marker"
        )

    # cover the modified canvas with a semi-transparent red tint and game-over text
    def draw_gameover_overlay(self):
        canvas = self.widgets["mod_canvas"]
        cx, cy = self.CANVAS_W // 2, self.CANVAS_H // 2

        canvas.create_rectangle(
            0,
            0,
            self.CANVAS_W,
            self.CANVAS_H,
            fill="#A32D2D",
            stipple="gray25",  # stipple = dotted fill, gives transparency effect
            outline="",
            tags="overlay"
        )

        text = "Game over" if self._ended_by_reveal else "Game over — 3 mistakes"
        canvas.create_text(
            cx,
            cy,
            text=text,
            fill="#FCEBEB",
            font=("Segoe UI", 11, "bold"),
            tags="overlay"
        )

    # ================= EVENT HANDLERS =================

    # open file picker, start a new game with the chosen image
    def on_load(self):
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return  # user cancelled the dialog

        try:
            self.game_manager.start_new_game(
                path,
                self.CANVAS_W,
                self.CANVAS_H
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))
            return

        self._ended_by_reveal = False
        self.sv["filename"].set(os.path.basename(path))
        self.widgets["button_load"].config(text="Load next image")

        self.display_images()
        self.refresh_state()

    # handle player click on modified canvas — hit or miss
    def on_canvas_click(self, event):
        if self.game_manager.game_state != "playing":
            return

        x, y = event.x, event.y

        difference = self.game_manager.check_click(x, y)

        if difference is not None:
            # hit — draw circle and check if the game is now over
            cx, cy = difference.center()
            self.draw_found_circle(cx, cy, difference.radius())

            if self.game_manager.game_state == "victory":
                self.refresh_state()
                messagebox.showinfo(
                    "Congratulations!",
                    "You found all 5 differences!"
                )
            else:
                self.refresh_state()

        else:
            # miss — show X and update mistake counter
            self.draw_wrong_click(x, y)
                # If this wrong click caused game over,
            # show all remaining differences with blue circles
            if self.game_manager.game_state == "game_over":
                for difference in self.game_manager.get_unfound_differences():
                    cx, cy = difference.center()
                    self.draw_reveal_circle(cx, cy, difference.radius())
            self.refresh_state()

    # confirm then reveal all unfound differences and end the game
    def on_reveal(self):
        if self.game_manager.game_state != "playing":
            return

        # ask before spoiling — one accidental click shouldn't end the game
        answer = messagebox.askyesno(
            "Reveal",
            "Reveal all unfound differences?\nThis will end the current game."
        )

        if not answer:
            return

        for difference in self.game_manager.get_unfound_differences():
            cx, cy = difference.center()
            self.draw_reveal_circle(cx, cy, difference.radius())

        self._ended_by_reveal = True
        self.game_manager.game_state = "game_over"
        self.refresh_state()

if __name__ == "__main__":
    SpotTheDifferenceApp()