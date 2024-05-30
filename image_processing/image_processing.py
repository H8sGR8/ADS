from PIL import Image
import numpy as np
from time import time
from tqdm import tqdm


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

    def mean_filter(self, size: tuple[int, int]) -> None:
        pixels = np.array(self.image.convert("L"), dtype=np.uint8)
        area = size[0] * size[1]
        horizontal_padding = size[0]//2
        vertical_padding = size[1]//2
        new_pixels = []
        for y in tqdm(range(vertical_padding, self.image.height - vertical_padding)):
            new_pixels_line = []
            for x in range(horizontal_padding, self.image.width - horizontal_padding):
                pixel = 0
                for y_size in range(-vertical_padding, vertical_padding):
                    for x_size in range(-horizontal_padding, horizontal_padding):
                        pixel += pixels[y + y_size][x + x_size]
                new_pixels_line.append(pixel // area)
            new_pixels.append(new_pixels_line)
        Image.fromarray(np.array(new_pixels)).show()

    def create_summed_area_table(self) -> np.ndarray:
        sat = np.array(self.image.convert("L"), dtype=int)
        for y in range(self.image.height):
            for x in range(self.image.width):
                if x > 0 and y > 0:
                    sat[y][x] += sat[y][x - 1] - sat[y - 1][x - 1] + sat[y - 1][x]
                elif x > 0:
                    sat[y][x] += sat[y][x - 1]
                elif y > 0:
                    sat[y][x] += sat[y - 1][x]
        return sat

    def mean_filter_with_summed_area_table(self, size: tuple[int, int]) -> None:
        sat = self.create_summed_area_table()
        area = size[0] * size[1]
        horizontal_padding = size[0] // 2
        vertical_padding = size[1] // 2
        new_pixels = []
        for y in range(vertical_padding, self.image.height - vertical_padding):
            new_pixels_line = []
            for x in range(horizontal_padding, self.image.width - horizontal_padding):
                new_pixels_line.append((sat[y + vertical_padding][x + horizontal_padding] -
                                        sat[y + vertical_padding][x - horizontal_padding] -
                                        sat[y - vertical_padding][x + horizontal_padding] +
                                        sat[y - vertical_padding][x - horizontal_padding]) // area)
            new_pixels.append(new_pixels_line)
        Image.fromarray(np.array(new_pixels)).show()

    def grayscale_with_mean_filter(self, naive: bool, size: tuple[int, int]) -> None:
        if naive:
            self.mean_filter(size)
        else:
            self.mean_filter_with_summed_area_table(size)


if __name__ == "__main__":
    yoda = ReadingImage("yoda.jpeg")
    sudoku = ReadingImage("sudoku.jpg")
    road = ReadingImage("road.jpg")
    sudoku.global_single_thresholding(127, True)
    sudoku.local_single_thresholding()
    yoda.global_single_thresholding(127, True)
    yoda.double_thresholding(120, 220, "white")
    yoda.grayscale_with_histogram()
    t1 = time()
    road.grayscale_with_mean_filter(True, (5, 5))
    t2 = time()
    road.grayscale_with_mean_filter(False, (21, 21))
    print(f"for naive method time is {t2 - t1}, for sat method time is {time() - t2}")
