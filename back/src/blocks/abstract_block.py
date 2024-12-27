from cv2.typing import MatLike
from abc import abstractmethod
from back.src.fruits import DetectedFruits


class AbstractBlock:
    @abstractmethod
    def __init__(self, cv_image: MatLike):
        pass

    @abstractmethod
    def get_result(self) -> DetectedFruits:
        pass
