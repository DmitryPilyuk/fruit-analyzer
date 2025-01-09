from back.src.models.training_scripts.model_utils import infer
from feature_groups import FeatureGroups
import joblib

color_model = joblib.load("../FeatureGroups.COLOR.pkl")
structure_model = joblib.load("../FeatureGroups.STRUCTURE.pkl")
leaf_model = joblib.load("../FeatureGroups.LEAF.pkl")
shape_model = joblib.load("../FeatureGroups.SHAPE.pkl")
texture_model = joblib.load("../FeatureGroups.TEXTURE.pkl")
high_accuracy_model = joblib.load("../87_leaf_features.pkl")

models = {
    color_model: FeatureGroups.COLOR,
    structure_model: FeatureGroups.STRUCTURE,
    texture_model: FeatureGroups.TEXTURE,
    leaf_model: FeatureGroups.LEAF,
    shape_model: FeatureGroups.SHAPE,
    high_accuracy_model: FeatureGroups.ALL,
}


# test the model
TEST_IMAGE_PATH = "/home/alex/dev/uni/classifier/model/test_images/watermelon.jpeg"
DATASET_PATH = "/home/alex/dev/uni/dataset_v2"

for model in models:
    feature_group = models[model]
    result = infer(model, TEST_IMAGE_PATH, feature_group)
    print(feature_group)
    print(f"Predicted Label ({TEST_IMAGE_PATH}): {result['predicted_label']}")
    print("Probabilities:")
    for label, prob in result["probabilities"].items():
        print(f"  {label}: {prob:.2f}")
