import cv2

from back.src.blocks.color import AbstractBlock


class TextureBlock(AbstractBlock):
    def __init__(self, cv_image):
        super().__init__(cv_image)
        self.__variance = self.__count_variance()
        self.__smooth_texture_flag = self.__is_smooth()

    def get_result(self):
        self.__set_detected_fruits()
        return super().get_result()

    def __set_detected_fruits(self):
        if self.__smooth_texture_flag:
            self.detected_fruits.Apple = True
            self.detected_fruits.Banana = True

    def __is_smooth(self):
        return True if self.__variance < 1500 else False

    def __count_variance(self):
        cv_gray = cv2.resize(
            cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY), (128, 128)
        )
        laplacian = cv2.Laplacian(cv_gray, cv2.CV_64F)
        return laplacian.var()
