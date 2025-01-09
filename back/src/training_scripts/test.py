from src.training_scripts.model_utils import infer
from feature_groups import FeatureGroups
import joblib

color_model = joblib.load("models/FeatureGroups.COLOR.pkl")
structure_model = joblib.load("models/FeatureGroups.STRUCTURE.pkl")
leaf_model = joblib.load("models/FeatureGroups.LEAF.pkl")
shape_model = joblib.load("models/FeatureGroups.SHAPE.pkl")
texture_model = joblib.load("models/FeatureGroups.TEXTURE.pkl")
high_accuracy_model = joblib.load("models/main_model.pkl")

models = {
    color_model: FeatureGroups.COLOR,
    structure_model: FeatureGroups.STRUCTURE,
    texture_model: FeatureGroups.TEXTURE,
    leaf_model: FeatureGroups.LEAF,
    shape_model: FeatureGroups.SHAPE,
    high_accuracy_model: FeatureGroups.ALL,
}


# test the models
TEST_IMAGE_PATH = "path/to/test/image"

for model in models:
    feature_group = models[model]
    result = infer(model, TEST_IMAGE_PATH, feature_group)
    print(feature_group)
    print(f"Predicted Label ({TEST_IMAGE_PATH}): {result['predicted_label']}")
    print("Probabilities:")
    for label, prob in result["probabilities"].items():
        print(f"  {label}: {prob:.2f}")
