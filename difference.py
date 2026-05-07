import cv2
import numpy as np
import random

class Difference:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.is_found = False

    def is_clicked(self, px, py):
        #Check if the clicks (px, py) are within the rectangle.
        return (self.x <= px <= self.x + self.w) and (self.y <= py <= self.y + self.h)

    def intersects(self, other):
        #Checking for overlap using the AABB (Axis-Aligned Bounding Box) algorithm
        #Two rectangles do NOT intersect if one lies entirely on one side of the other.
        return not (self.x + self.w < other.x or 
                    other.x + other.w < self.x or 
                    self.y + self.h < other.y or 
                    other.y + other.h < self.y)

    def apply(self, image):
        #Abstract functions must be overridden by their subclasses
        raise NotImplementedError("Subclasses must implement apply()")


class ColorShiftDiff(Difference):
    def apply(self, image):
        #Choose the ROI (Region of Interest) region
        roi = image[self.y:self.y+self.h, self.x:self.x+self.w]
        # Shift color red slightly up, use cv2.add to avoid overflow
        image[self.y:self.y+self.h, self.x:self.x+self.w] = cv2.add(roi, np.array([0, 0, 50], dtype=np.uint8))

class BlurDiff(Difference):
    def apply(self, image):
        roi = image[self.y:self.y+self.h, self.x:self.x+self.w]
        #Gaussian blur with a 15x15 kernel
        image[self.y:self.y+self.h, self.x:self.x+self.w] = cv2.GaussianBlur(roi, (15, 15), 0)

class BrightnessDiff(Difference):
    def apply(self, image):
        roi = image[self.y:self.y+self.h, self.x:self.x+self.w]
        #Increase brightness by matrix addition
        image[self.y:self.y+self.h, self.x:self.x+self.w] = cv2.add(roi, np.array([40, 40, 40], dtype=np.uint8))