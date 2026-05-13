"""
game_manager.py

Requires:
    pip install opencv-python pillow numpy
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import random
import cv2
import numpy as np


Point = Tuple[int, int]
BGRColor = Tuple[int, int, int]


@dataclass
class DifferenceRegion:
    """Stores one generated difference region."""
    id: int
    x: int
    y: int
    radius: int
    alteration_type: str
    found: bool = False
    revealed: bool = False

    def contains(self, px: int, py: int, tolerance: int = 12) -> bool:
        """Return True if a click is close enough to this region."""
        dx = px - self.x
        dy = py - self.y
        return (dx * dx + dy * dy) <= (self.radius + tolerance) ** 2

    def bbox(self) -> Tuple[int, int, int, int]:
        """Return bounding box as x1, y1, x2, y2."""
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )


class ImageAlteration:
    """Base class for OpenCV image alterations."""

    name = "base"

    def apply(self, image: np.ndarray, region: DifferenceRegion) -> None:
        raise NotImplementedError("Subclasses must implement apply().")


class ColourShiftAlteration(ImageAlteration):
    """Slightly changes colour in a circular region."""

    name = "colour_shift"

    def apply(self, image: np.ndarray, region: DifferenceRegion) -> None:
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (region.x, region.y), region.radius, 255, -1)

        shift = np.array(
            [random.randint(-25, 25), random.randint(-25, 25), random.randint(-25, 25)],
            dtype=np.int16,
        )

        area = image[mask == 255].astype(np.int16)
        area = np.clip(area + shift, 0, 255).astype(np.uint8)
        image[mask == 255] = area


class BlurAlteration(ImageAlteration):
    """Applies local blur to one region."""

    name = "local_blur"

    def apply(self, image: np.ndarray, region: DifferenceRegion) -> None:
        x1, y1, x2, y2 = _clip_bbox(region.bbox(), image.shape[1], image.shape[0])
        roi = image[y1:y2, x1:x2]
        if roi.size == 0:
            return

        blurred = cv2.GaussianBlur(roi, (15, 15), 0)

        mask = np.zeros((y2 - y1, x2 - x1), dtype=np.uint8)
        cv2.circle(mask, (region.x - x1, region.y - y1), region.radius, 255, -1)
        roi[mask == 255] = blurred[mask == 255]


class BrightnessAlteration(ImageAlteration):
    """Makes one region slightly brighter or darker."""

    name = "brightness_change"

    def apply(self, image: np.ndarray, region: DifferenceRegion) -> None:
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (region.x, region.y), region.radius, 255, -1)

        change = random.choice([-35, -25, 25, 35])
        area = image[mask == 255].astype(np.int16)
        area = np.clip(area + change, 0, 255).astype(np.uint8)
        image[mask == 255] = area


# my individual task gaemanager line 111- 352

class GameManager:
    """
    Main portable game manager.

    Responsibilities:
    - Load original image
    - Create modified clone using OpenCV
    - Generate exactly 5 non-overlapping differences
    - Validate clicks
    - Track remaining differences and mistakes
    - Reveal unfound differences
    """

    DIFFERENCE_COUNT = 5
    MAX_MISTAKES = 3

    def __init__(self, difference_count: int = DIFFERENCE_COUNT, max_mistakes: int = MAX_MISTAKES):
        self.difference_count = difference_count
        self.max_mistakes = max_mistakes

        self.original_image: Optional[np.ndarray] = None
        self.modified_image: Optional[np.ndarray] = None
        self.display_scale: float = 1.0

        self.regions: List[DifferenceRegion] = []
        self.mistakes: int = 0
        self.game_over: bool = False

        self.alterations: List[ImageAlteration] = [
            ColourShiftAlteration(),
            BlurAlteration(),
            BrightnessAlteration(),
        ]

    def load_image(self, image_path: str) -> Dict:
        """
        Load image and generate new random differences.

        Returns a state dictionary for GUI use.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image. Please use JPG, PNG, or BMP.")

        self.original_image = image
        self.modified_image = image.copy()
        self.regions = []
        self.mistakes = 0
        self.game_over = False

        self._generate_difference_regions()
        self._apply_differences()

        return self.get_state()

    def set_display_scale(self, scale: float) -> None:
        """
        Set scale used by GUI display.

        """
        if scale <= 0:
            raise ValueError("Display scale must be greater than 0.")
        self.display_scale = scale

    def handle_click(self, x_display: int, y_display: int) -> Dict:
        """
        Validate player's click on modified image.

        x_display and y_display are coordinates from the displayed GUI image.
        Returns a result dictionary.
        """
        if self.original_image is None or self.modified_image is None:
            return {"status": "no_image", "message": "Please load an image first.", **self.get_state()}

        if self.game_over:
            return {"status": "game_over", "message": "Game over. Load a new image.", **self.get_state()}

        x = int(x_display / self.display_scale)
        y = int(y_display / self.display_scale)

        for region in self.regions:
            if not region.found and not region.revealed and region.contains(x, y):
                region.found = True

                if self.remaining_count() == 0:
                    self.game_over = True
                    return {
                        "status": "found_all",
                        "message": "Congratulations! You found all 5 differences.",
                        "region": region,
                        **self.get_state(),
                    }

                return {
                    "status": "correct",
                    "message": f"Correct! Remaining: {self.remaining_count()}",
                    "region": region,
                    **self.get_state(),
                }

        self.mistakes += 1

        if self.mistakes >= self.max_mistakes:
            self.game_over = True
            return {
                "status": "too_many_mistakes",
                "message": "You reached 3 mistakes. Load a new image or reveal the answer.",
                **self.get_state(),
            }

        return {
            "status": "wrong",
            "message": f"Wrong click. Mistakes: {self.mistakes}/{self.max_mistakes}",
            **self.get_state(),
        }

    def reveal_unfound(self) -> Dict:
        """
        Reveal all currently unfound differences.
        GUI should draw these with blue circles.
        """
        if self.original_image is None:
            return {"status": "no_image", "message": "Please load an image first.", **self.get_state()}

        for region in self.regions:
            if not region.found:
                region.revealed = True

        self.game_over = True
        return {
            "status": "revealed",
            "message": "All unfound differences have been revealed.",
            **self.get_state(),
        }

    def remaining_count(self) -> int:
        """Return number of differences not found and not revealed."""
        return sum(1 for r in self.regions if not r.found and not r.revealed)

    def found_regions(self) -> List[DifferenceRegion]:
        return [r for r in self.regions if r.found]

    def revealed_regions(self) -> List[DifferenceRegion]:
        return [r for r in self.regions if r.revealed]

    def get_state(self) -> Dict:
        """Return current game state for GUI/status labels."""
        return {
            "remaining": self.remaining_count(),
            "mistakes": self.mistakes,
            "max_mistakes": self.max_mistakes,
            "game_over": self.game_over,
            "regions": self.regions,
            "found_regions": self.found_regions(),
            "revealed_regions": self.revealed_regions(),
        }

    def get_original_rgb(self) -> np.ndarray:
        """Return original image in RGB for Tkinter/Pillow display."""
        self._require_image()
        return cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

    def get_modified_rgb(self) -> np.ndarray:
        """Return modified image in RGB for Tkinter/Pillow display."""
        self._require_image()
        return cv2.cvtColor(self.modified_image, cv2.COLOR_BGR2RGB)

    def draw_markers_for_display(self, image_rgb: np.ndarray, side: str = "modified") -> np.ndarray:
        """
        Optional helper for GUI.

        Draws:
        - red circles for found differences
        - blue circles for revealed differences

        side parameter is kept for readability; both original and modified can be marked.
        """
        output = image_rgb.copy()

        for region in self.found_regions():
            cv2.circle(output, (region.x, region.y), region.radius + 4, (255, 0, 0), 3)

        for region in self.revealed_regions():
            cv2.circle(output, (region.x, region.y), region.radius + 4, (0, 0, 255), 3)

        return output

    def _generate_difference_regions(self) -> None:
        self._require_image()
        height, width = self.original_image.shape[:2]

        min_dimension = min(width, height)
        radius_min = max(12, min_dimension // 35)
        radius_max = max(radius_min + 2, min_dimension // 18)
        margin = radius_max + 10

        attempts = 0
        max_attempts = 1000

        while len(self.regions) < self.difference_count and attempts < max_attempts:
            attempts += 1

            radius = random.randint(radius_min, radius_max)
            x = random.randint(margin, width - margin)
            y = random.randint(margin, height - margin)

            candidate = DifferenceRegion(
                id=len(self.regions) + 1,
                x=x,
                y=y,
                radius=radius,
                alteration_type="pending",
            )

            if self._is_non_overlapping(candidate):
                self.regions.append(candidate)

        if len(self.regions) < self.difference_count:
            raise RuntimeError("Image is too small to place 5 non-overlapping differences.")

    def _apply_differences(self) -> None:
        self._require_image()

        for region in self.regions:
            alteration = random.choice(self.alterations)
            region.alteration_type = alteration.name
            alteration.apply(self.modified_image, region)

    def _is_non_overlapping(self, candidate: DifferenceRegion) -> bool:
        for existing in self.regions:
            dx = candidate.x - existing.x
            dy = candidate.y - existing.y
            minimum_distance = candidate.radius + existing.radius + 25
            if (dx * dx + dy * dy) < minimum_distance * minimum_distance:
                return False
        return True

    def _require_image(self) -> None:
        if self.original_image is None or self.modified_image is None:
            raise ValueError("No image loaded.")


def _clip_bbox(bbox: Tuple[int, int, int, int], width: int, height: int) -> Tuple[int, int, int, int]:
    x1, y1, x2, y2 = bbox
    return max(0, x1), max(0, y1), min(width, x2), min(height, y2)