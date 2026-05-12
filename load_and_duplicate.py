import cv2

class ImageProcessor:
    def __init__(self, target_width=500, target_height=500):
        self.target_w = target_width
        self.target_h = target_height

    def load_and_scale(self, file_path):
        # step 1: load img and resize it to the correct ratio
        # read img from a link (support JPG, PNG, BMP) 
        original = cv2.imread(file_path)
        if original is None:
            return None

        # calculate the ration to avoid img distortion 
        h, w = original.shape[:2]
        # formula: ratio = min(W_target / W_origin, H_target / H_origin)
        ratio = min(self.target_w / w, self.target_h / h)
        new_size = (int(w * ratio), int(h * ratio))

        # resize the img according to the calculated aspect ratio 
        scaled_img = cv2.resize(original, new_size, interpolation=cv2.INTER_AREA)
        return scaled_img

    def duplicate_and_modify(self, scaled_img):
        # step 2: duplicate and prepare to create 5 differences
        # create an exact copy from the scaled img
        modified_img = scaled_img.copy() 
        
        # note: 5 differences will be added to this copy
        # (here call functions to create Color, Shift, Blur,...)
        
        return modified_img