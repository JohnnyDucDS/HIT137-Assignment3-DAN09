import cv2
import random
import numpy as np
from PIL import Image

class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.modified_image = None
        self.differences = []

    def load_image(self, file_path):
        try:
            # PIL can open jpg, png, bmp more reliably
            pil_image = Image.open(file_path).convert("RGB")
    
            # PIL uses RGB, OpenCV uses BGR
            self.original_image = cv2.cvtColor(
                np.array(pil_image),
                cv2.COLOR_RGB2BGR
            )
    
        except Exception:
            raise ValueError("Image could not be loaded")
    
        self.modified_image = self.original_image.copy()
        self.differences = []

    def create_modified_image(self):
        for _ in range(5):
            difference = self.generate_non_overlapping_difference()
            self.differences.append(difference)
            self.apply_alteration(difference)

    def generate_non_overlapping_difference(self):
        image_height, image_width = self.original_image.shape[:2]   # => get 2 first elemts but the chanel
        while True:
            width = random.randint(40, 80)  # 40 80 to not touch frame
            height = random.randint(40, 80)

            x = random.randint(0, image_width - width)    
            y = random.randint(0, image_height - height)

            alteration_type = random.choice([
                "colour_shift",
                "blur",
                "brightness"    # add slip method?
            ])

            new_difference = Difference(x, y, width, height, alteration_type)

            overlap = False
            for existing_difference in self.differences:
                if new_difference.overlaps_with(existing_difference):
                    overlap = True
                    break

            if not overlap:
                return new_difference

    def apply_alteration(self, difference):
        if difference.alteration_type == "colour_shift":
            self.apply_colour_shift(difference)

        elif difference.alteration_type == "blur":
            self.apply_blur(difference)

        elif difference.alteration_type == "brightness":
            self.apply_brightness_change(difference)

    def get_region(self, difference):
        return self.modified_image[
            difference.y:difference.y + difference.height,  # ?
            difference.x:difference.x + difference.width    # => from x to x+width
        ]


    def apply_colour_shift(self, difference):
        region = self.get_region(difference)

        channel = random.randint(0, 2)
        shift = random.randint(-50, 50)    # apply darker or brighter

        region[:, :, channel] = cv2.add(
            region[:, :, channel],          #more colour-ish
            shift
        )

    def apply_blur(self, difference):
        region = self.get_region(difference)

        blurred_region = cv2.GaussianBlur(region, (15, 15), 0) 
        self.modified_image[
            difference.y:difference.y + difference.height,
            difference.x:difference.x + difference.width
        ] = blurred_region

    def apply_brightness_change(self, difference):
        region = self.get_region(difference)

        brighter_region = cv2.convertScaleAbs(region, alpha=1.0, beta=40) #new_pixel = abs(alpha * pixel + beta)
        self.modified_image[
            difference.y:difference.y + difference.height,
            difference.x:difference.x + difference.width
            ] = brighter_region


processor = ImageProcessor()

processor.load_image("image.jpg")
processor.create_modified_image()

cv2.imshow("Original", processor.original_image)
cv2.imshow("Modified", processor.modified_image)

cv2.waitKey(0)          # wait untill action / otherwise window open and close 
cv2.destroyAllWindows()

cv2.imwrite("modified_output.png", processor.modified_image)

print(processor.original_image)   # original image data
print(processor.modified_image)   # changed image data
print(processor.differences)      # list of 5 Difference objects
