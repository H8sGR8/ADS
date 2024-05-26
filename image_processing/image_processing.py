from PIL import Image
import numpy as np


class ReadingImage:

    def __init__(self, image):
        self.image = Image.open(image)

    def set_min_max_mean_of_intensity(self):
        pixels = np.array(self.image)
        pixels_intensity = []
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel_intensity = (pixels[y][x][0] // 3 + pixels[y][x][1] // 3 + pixels[y][x][2] // 3)
                pixels_intensity.append(pixel_intensity)
                pixels[y][x] = [pixel_intensity, pixel_intensity, pixel_intensity]
        pixels_intensity.sort()
        return (min(pixels_intensity), max(pixels_intensity),
                pixels_intensity[len(pixels_intensity)//2], pixels, pixels_intensity)

    def global_single_thresholding(self, limit):
        pixels = np.array(self.image)
        for y in range(self.image.height):
            for x in range(self.image.width):
                if (pixels[y][x][0] / 3 + pixels[y][x][1] / 3 + pixels[y][x][2] / 3) < limit:
                    pixels[y][x] = [0, 0, 0]
                else:
                    pixels[y][x] = [255, 255, 255]
        Image.fromarray(pixels).show()

    def local_single_thresholding(self):
        min_intensity, max_intensity, mean, _, _ = self.set_min_max_mean_of_intensity()
        limit = (max_intensity + min_intensity - mean) // 2
        self.global_single_thresholding(limit)

    def double_thresholding(self, bottom, top, color):
        pixels = np.array(self.image)
        for y in range(self.image.height):
            for x in range(self.image.width):
                if bottom < (pixels[y][x][0]/3 + pixels[y][x][1]/3 + pixels[y][x][2]/3) < top:
                    if color == "black":
                        pixels[y][x] = [0, 0, 0]
                    elif color == "white":
                        pixels[y][x] = [255, 255, 255]
                    else:
                        print("wrong color")
                        return
                else:
                    if color == "black":
                        pixels[y][x] = [255, 255, 255]
                    elif color == "white":
                        pixels[y][x] = [0, 0, 0]
                    else:
                        print("wrong color")
                        return
        Image.fromarray(pixels).show()

    @staticmethod
    def count_cfd(number_of_pixels, various_elements, looking_for):
        count = 0
        for i in various_elements:
            count += number_of_pixels.count(i)
            if i == looking_for:
                break
        return count

    def grayscale_with_histogram(self):
        min_intensity, max_intensity, _, pixels, number_of_pixels = self.set_min_max_mean_of_intensity()
        Image.fromarray(pixels).show()
        various_elements = {x for x in number_of_pixels}
        cfd_dict = {x: 255 * (self.count_cfd(number_of_pixels, various_elements, x) -
                              self.count_cfd(number_of_pixels, various_elements, min_intensity)) /
                             (len(number_of_pixels) -
                              self.count_cfd(number_of_pixels, various_elements, min_intensity))
                    for x in various_elements}
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel_intensity = cfd_dict[pixels[y][x][0]]
                pixels[y][x] = [pixel_intensity, pixel_intensity, pixel_intensity]
        Image.fromarray(pixels).show()


if __name__ == "__main__":
    yoda = ReadingImage("yoda.jpeg")
    sudoku = ReadingImage("sudokubig.jpg")
    sudoku.global_single_thresholding(127)
    sudoku.local_single_thresholding()
    '''yoda.global_single_thresholding(127)
    yoda.double_thresholding(140, 190, "white")
    yoda.grayscale_with_histogram()'''
