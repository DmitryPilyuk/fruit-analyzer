from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DetectedFruits:
    Banana: bool = False
    Apple: bool = False
    Grapes: bool = False
    Orange: bool = False 
    Pineapple: bool = False


def estimate_fruit_probability(*detected_list: List[DetectedFruits]) -> Dict[str, str]:
    """Calculates the probability of each fruit being detected across a list of DetectedFruits instances.

    Args:
        detected_list: A list of DetectedFruits instances.

    Returns:
        A dictionary where keys are fruit names and values are their detection probabilities as float numbers.
    """
    if not detected_list or len(detected_list) == 0:
        return {}

    total_instances = 0 # count of recognized fruits

    # dict with every fruit count
    fruit_counts = {field: 0 for field in DetectedFruits.__annotations__}

    # fill dict
    for detected_fruits in detected_list:
        for fruit, detected in detected_fruits.__dict__.items():
            if detected:
                total_instances += 1
                fruit_counts[fruit] += 1

    # count probabilities
    probabilities = {}
    for fruit, count in fruit_counts.items():
        probability = (count / total_instances) * 100.0
        probabilities[fruit] = probability

    return probabilities