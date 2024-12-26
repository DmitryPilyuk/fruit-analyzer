from dataclasses import dataclass

@dataclass
class DetectedFruits:
    Banana: bool = False
    Apple: bool = False
    Grapes: bool = False
    Orange: bool = False 
    Pineapple: bool = False