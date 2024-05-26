from PIL import Image
import numpy as np


class ReadingImage:

    def __init__(self, image):
        self.image = Image.open(image).convert("RGB")

    def global_single_thresholding(self, limit, show):
        pixels = np.array(self.image.convert("L"))
        if show:
            Image.fromarray(np.where(pixels < limit, 0, 255)).show()
        else:
            return np.where(pixels < limit, 0, 255)

    def local_single_thresholding(self):
        pixels = np.array(self.image.convert("L"))
        limit = (pixels.min() + pixels.max() - pixels.mean()) // 2
        self.global_single_thresholding(limit, True)

    def double_thresholding(self, bottom, top, color):
        bottom_threshold = self.global_single_thresholding(bottom, False)
        top_threshold = self.global_single_thresholding(top, False)
        if color == "black":
            Image.fromarray(np.where(bottom_threshold != top_threshold, 0, 255)).show()
        elif color == "white":
            Image.fromarray(np.where(bottom_threshold != top_threshold, 255, 0)).show()
        else:
            print("wrong color")

    def grayscale_with_histogram(self):
        pixels = np.array(self.image.convert("L"))
        various_elements, count = np.unique(pixels, return_counts=True)
        cfd_dict = {}
        for i in range(len(various_elements)):
            if i == 0:
                cfd_dict[pixels.min()] = count[i]
            else:
                cfd_dict[various_elements[i]] = count[i] + cfd_dict[various_elements[i - 1]]
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixels[y][x] = round(255 * ((cfd_dict[pixels[y][x]] - cfd_dict[min(various_elements)]) /
                                     (pixels.size - cfd_dict[min(various_elements)])))
        Image.fromarray(pixels).show()


if __name__ == "__main__":
    yoda = ReadingImage("yoda.jpeg")
    sudoku = ReadingImage("sudoku.jpg")
    sudoku.global_single_thresholding(127, True)
    sudoku.local_single_thresholding()
    yoda.global_single_thresholding(127, True)
    yoda.double_thresholding(120, 220, "white")
    yoda.grayscale_with_histogram()
