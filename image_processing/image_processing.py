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
        Image.fromarray(self.global_single_thresholding(limit, False)).show()

    def double_thresholding(self, bottom, top, color):
        bottom_threshold = self.global_single_thresholding(bottom, False)
        top_threshold = self.global_single_thresholding(top, False)
        if color == "black":
            Image.fromarray(np.where(bottom_threshold != top_threshold, 0, 255)).show()
        elif color == "white":
            Image.fromarray(np.where(bottom_threshold != top_threshold, 255, 0)).show()
        else:
            print("wrong color")

    def create_greyscale(self):
        pixels = np.array(self.image)
        pixels_intensity = []
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel_intensity = (pixels[y][x][0] // 3 + pixels[y][x][1] // 3 + pixels[y][x][2] // 3)
                pixels_intensity.append(pixel_intensity)
                pixels[y][x] = [pixel_intensity, pixel_intensity, pixel_intensity]
        pixels_intensity.sort()
        return (min(pixels_intensity), max(pixels_intensity),
                pixels_intensity[len(pixels_intensity) // 2], pixels, pixels_intensity)

    def grayscale_with_histogram(self):
        min_intensity, _, _, pixels, number_of_pixels = self.create_greyscale()
        various_elements = list({x for x in number_of_pixels})
        cfd_dict = {}
        for i in range(len(various_elements)):
            if i == 0:
                cfd_dict[min_intensity] = number_of_pixels.count(min_intensity)
            else:
                cfd_dict[various_elements[i]] = (
                        number_of_pixels.count(various_elements[i]) + cfd_dict[various_elements[i - 1]])
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel_intensity = (255 * (cfd_dict[pixels[y][x][0]] - cfd_dict[min_intensity]) //
                                   (len(number_of_pixels) - cfd_dict[min_intensity]))
                pixels[y][x] = [pixel_intensity, pixel_intensity, pixel_intensity]
        Image.fromarray(pixels).show()


if __name__ == "__main__":
    yoda = ReadingImage("yoda.jpeg")
    sudoku = ReadingImage("sudokubig.jpg")
    # sudoku.global_single_thresholding(127, True)
    # sudoku.local_single_thresholding()
    # yoda.global_single_thresholding(127, True)
    # yoda.double_thresholding(120, 220, "white")
    yoda.grayscale_with_histogram()
