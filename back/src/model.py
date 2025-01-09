import joblib
from models.training_scripts.feature_groups import FeatureGroups
from models.training_scripts.model_utils import infer


class Model:
    def __init__(self, model_path, faeture_groups: FeatureGroups):
        self.model = joblib.load(model_path)
        self.feature_group = faeture_groups

    def get_predictions(self, image_path):
        return infer(self.model, image_path, self.feature_group)
