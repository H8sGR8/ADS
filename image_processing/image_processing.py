from PIL import Image
import numpy as np


class ReadingImage:

    def __init__(self, image):
        self.image = Image.open(image)
        self.pixels = np.array(self.image)

    def show_image(self):
        Image.fromarray(self.pixels).show()


if __name__ == "__main__":
    yoda = ReadingImage("yoda.jpeg")
    yoda.show_image()
