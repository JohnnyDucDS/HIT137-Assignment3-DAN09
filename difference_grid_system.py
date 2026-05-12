# This method divides the image into a grid (for example, a 3x3 grid with 9 large cells).
# Logic: randomly select 5 cells from those 9. In each cell, I place a small error region.
# advantage: I don't need to use the complex AABB algorithm at all to achieve the "non-overlapping" requirement of the problem.

class Difference:
    def __init__(self, cell_x, cell_y, cell_w, cell_h):
        # 1. Identify the location of random errors INSIDE the assigned grid cell
        # This method ensures that errors never jump outside the cell, guaranteeing no overlap.
        self.w = 40 # Fixed width of the error area
        self.h = 40 # Fixed height of the error area
        
        
        # The x and y coordinates will be randomly located within that cell.
        import random
        self.x = random.randint(cell_x, cell_x + cell_w - self.w)
        self.y = random.randint(cell_y, cell_y + cell_h - self.h)
        
        self.is_found = False # The initial state is not found

    def is_clicked(self, px, py):
        # Check if the click coordinates (px, py) are within the error area
        # We allow a small margin of error (e.g., +10 pixels) so that the player can easily click the correct button
        tolerance = 10
        return (self.x - tolerance <= px <= self.x + self.w + tolerance) and \
               (self.y - tolerance <= py <= self.y + self.h + tolerance)

    def apply(self, image):
        pass