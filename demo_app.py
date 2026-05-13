"""
demo_app.py
Small Tkinter demo showing how teammates can integrate game_manager.py.

Run:
    python demo_app.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

from game_manager import GameManager


class SpotDifferenceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("HIT137 Spot the Difference - Game Manager Demo")
        self.geometry("1200x750")

        self.manager = GameManager()
        self.max_display_width = 520
        self.photo_left = None
        self.photo_right = None

        self._build_ui()

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(pady=10)

        tk.Button(top, text="Load Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Reveal", command=self.reveal).pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(top, text="Load an image to start.", font=("Arial", 12))
        self.status_label.pack(side=tk.LEFT, padx=20)

        image_frame = tk.Frame(self)
        image_frame.pack(expand=True, fill=tk.BOTH)

        left_frame = tk.Frame(image_frame)
        left_frame.pack(side=tk.LEFT, expand=True, padx=10)

        right_frame = tk.Frame(image_frame)
        right_frame.pack(side=tk.RIGHT, expand=True, padx=10)

        tk.Label(left_frame, text="Original Image").pack()
        tk.Label(right_frame, text="Modified Image - Click Here").pack()

        self.left_label = tk.Label(left_frame, bg="lightgrey")
        self.left_label.pack()

        self.right_label = tk.Label(right_frame, bg="lightgrey")
        self.right_label.pack()
        self.right_label.bind("<Button-1>", self.on_modified_click)

    def load_image(self):
        path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
            ],
        )

        if not path:
            return

        try:
            state = self.manager.load_image(path)
            self._update_images()
            self._update_status(f"Remaining: {state['remaining']} | Mistakes: 0/3")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_modified_click(self, event):
        result = self.manager.handle_click(event.x, event.y)
        self._update_images()
        self._update_status(
            f"{result['message']} | Remaining: {result['remaining']} | "
            f"Mistakes: {result['mistakes']}/{result['max_mistakes']}"
        )

        if result["status"] in ["found_all", "too_many_mistakes"]:
            messagebox.showinfo("Game Status", result["message"])

    def reveal(self):
        result = self.manager.reveal_unfound()
        self._update_images()
        self._update_status(
            f"{result['message']} | Remaining: {result['remaining']} | "
            f"Mistakes: {result['mistakes']}/{result['max_mistakes']}"
        )

    def _update_images(self):
        original = self.manager.get_original_rgb()
        modified = self.manager.get_modified_rgb()

        original = self.manager.draw_markers_for_display(original, side="original")
        modified = self.manager.draw_markers_for_display(modified, side="modified")

        original_pil, scale = self._resize_for_display(original)
        modified_pil, _ = self._resize_for_display(modified)

        self.manager.set_display_scale(scale)

        self.photo_left = ImageTk.PhotoImage(original_pil)
        self.photo_right = ImageTk.PhotoImage(modified_pil)

        self.left_label.configure(image=self.photo_left)
        self.right_label.configure(image=self.photo_right)

    def _resize_for_display(self, rgb_image):
        height, width = rgb_image.shape[:2]
        scale = min(1.0, self.max_display_width / width)
        new_width = int(width * scale)
        new_height = int(height * scale)

        resized = cv2.resize(rgb_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return Image.fromarray(resized), scale

    def _update_status(self, text):
        self.status_label.configure(text=text)


if __name__ == "__main__":
    app = SpotDifferenceApp()
    app.mainloop()