from PIL import Image
import numpy as np


class ReadingImage:

    def __init__(self, image):
        self.image = Image.open(image).convert("RGB")

    def global_single_thresholding(self, limit: int, show: bool) -> np.ndarray:
        pixels = np.array(self.image.convert("L"), dtype=np.uint8)
        if show:
            Image.fromarray(np.where(pixels < limit, 0, 255)).show()
        else:
            return np.where(pixels < limit, 0, 255)

    def local_single_thresholding(self) -> None:
        pixels = np.array(self.image.convert("L"), dtype=np.uint8)
        limit = (pixels.min() + pixels.max() - pixels.mean()) // 2
        self.global_single_thresholding(limit, True)

    def double_thresholding(self, bottom: int, top: int, color: str) -> None:
        bottom_threshold = self.global_single_thresholding(bottom, False)
        top_threshold = self.global_single_thresholding(top, False)
        if color == "black":
            Image.fromarray(np.where(bottom_threshold != top_threshold, 0, 255)).show()
        elif color == "white":
            Image.fromarray(np.where(bottom_threshold != top_threshold, 255, 0)).show()
        else:
            print("wrong color")

    def grayscale_with_histogram(self) -> None:
        pixels = np.array(self.image.convert("L"), dtype=np.uint8)
        various_elements, count = np.unique(pixels, return_counts=True)
        cfd_dict = {}
        new_pixel_values = {}
        for i in range(len(various_elements)):
            if i == 0:
                cfd_dict[pixels.min()] = count[i]
            else:
                cfd_dict[various_elements[i]] = count[i] + cfd_dict[various_elements[i - 1]]
        min_sum = cfd_dict[min(various_elements)]
        for i in range(len(various_elements)):
            new_pixel_values[various_elements[i]] = np.uint8(round((cfd_dict[various_elements[i]] - min_sum) /
                                                             (pixels.size - min_sum) * 255))
        Image.fromarray(np.array([new_pixel_values[np.uint8(x)]
                                  for x in np.nditer(pixels)]).reshape(self.image.height, self.image.width)).show()

    def grayscale_with_mean_filter(self, naive: bool):
        pass


if __name__ == "__main__":
    yoda = ReadingImage("yoda.jpeg")
    sudoku = ReadingImage("sudoku.jpg")
    '''sudoku.global_single_thresholding(127, True)
    sudoku.local_single_thresholding()
    yoda.global_single_thresholding(127, True)
    yoda.double_thresholding(120, 220, "white")'''
    yoda.grayscale_with_histogram()
