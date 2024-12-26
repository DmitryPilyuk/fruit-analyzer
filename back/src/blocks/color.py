import os
from dataclasses import dataclass

import cv2
import numpy as np

from back.src.blocks.abstract_block import AbstractBlock
from back.src.blocks.utils import get_limits
from back.src.fruits import DetectedFruits

img = cv2.imread(os.path.join(".", "grape_image.jpg"))


@dataclass
class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (0, 255, 255)
    ORANGE = (255, 165, 0)


class ColorBlock(AbstractBlock):
    def __init__(self, cv_image):
        self.color_limits = {
            Color.GREEN: get_limits(Color.GREEN),
            Color.RED: get_limits(Color.RED),
            Color.YELLOW: get_limits(Color.YELLOW),
            Color.ORANGE: get_limits(Color.ORANGE),
        }
        self.cv_image = cv_image
        self.__detected_fruits = DetectedFruits()

    def get_result(self):
        self.__set_detected_fruits()
        return self.__detected_fruits

    def __set_detected_fruits(self):
        most_popular_color = self.__get_most_popular_color()
        match most_popular_color:
            case Color.GREEN:
                self.__detected_fruits.Grapes = True
            case Color.RED:
                self.__detected_fruits.Apple = True
            case Color.YELLOW:
                self.__detected_fruits.Banana = True
            case Color.ORANGE:
                self.__detected_fruits.Orange = True

    def __get_most_popular_color(self):
        color_pixel = self.__get_pixels_number()
        return max(color_pixel, key=color_pixel.get)

    def __get_pixels_number(self):
        return {
            color: np.count_nonzero(cv2.inRange(self.cv_image, *limits))
            for color, limits in self.color_limits.items()
        }
