import joblib
from src.training_scripts.feature_groups import FeatureGroups
from src.training_scripts.model_utils import infer


class FruitAnalyzeModel:
    def __init__(self, model_path, faeture_groups: FeatureGroups):
        self.__model = joblib.load(model_path)
        self.__feature_group = faeture_groups

    def get_prediction(self, image_path):
        numpy_probabilities_dict = infer(
            self.__model, image_path, self.__feature_group
        )["probabilities"]

        output_dict = {
            str(key): float(value) for key, value in numpy_probabilities_dict.items()
        }
        return output_dict
