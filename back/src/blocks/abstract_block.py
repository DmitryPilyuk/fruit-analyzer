from cv2.typing import MatLike
from abc import abstractmethod
from back.src.fruits import DetectedFruits


class AbstractBlock:
    @abstractmethod
    def __init__(self, cv_image: MatLike):
        self.cv_image = cv_image
        self.detected_fruits = DetectedFruits()

    @abstractmethod
    def get_result(self) -> DetectedFruits:
        return self.detected_fruits
