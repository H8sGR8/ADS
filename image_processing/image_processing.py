from PIL import Image
import numpy as np


class ReadingImage:

    def __init__(self, image):
        self.image = Image.open(image)

    @staticmethod
    def show_image(array):
        Image.fromarray(array).show()

    def set_min_max_mean_of_intensity(self):
        pixels = np.array(self.image)
        pixels_intensity = []
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixels_intensity.append(round(pixels[y][x][0] / 3 + pixels[y][x][1] / 3 + pixels[y][x][2] / 3))
        pixels_intensity.sort()
        return min(pixels_intensity), max(pixels_intensity), pixels_intensity[len(pixels_intensity)//2]

    def global_single_thresholding(self, limit):
        pixels = np.array(self.image)
        for y in range(self.image.height):
            for x in range(self.image.width):
                if (pixels[y][x][0] / 3 + pixels[y][x][1] / 3 + pixels[y][x][2] / 3) < limit:
                    pixels[y][x] = [0, 0, 0]
                else:
                    pixels[y][x] = [255, 255, 255]
        self.show_image(pixels)

    def local_single_thresholding(self):
        pixels = np.array(self.image)
        min_intensity, _, mean = self.set_min_max_mean_of_intensity()
        for y in range(self.image.height):
            for x in range(self.image.width):
                if (pixels[y][x][0] / 3 + pixels[y][x][1] / 3 + pixels[y][x][2] / 3) < (min_intensity + mean) / 2:
                    pixels[y][x] = [0, 0, 0]
                else:
                    pixels[y][x] = [255, 255, 255]
        self.show_image(pixels)

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
        self.show_image(pixels)


if __name__ == "__main__":
    yoda = ReadingImage("yoda.jpeg")
    sudoku = ReadingImage("sudokubig.jpg")
    sudoku.global_single_thresholding(127)
    sudoku.local_single_thresholding()
    yoda.global_single_thresholding(127)
    yoda.double_thresholding(140, 190, "white")
