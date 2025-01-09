from src.training_scripts.model_utils import train_model, save_model
from feature_groups import FeatureGroups

models_dict = {}
PATH_TO_SAVE = ""  # adjust as needed
DATA_DIR = "path/to/dataset"


for feature_group in FeatureGroups:
    model = train_model(DATA_DIR, feature_group)
    models_dict[feature_group] = model
    save_model(model, f"{PATH_TO_SAVE}{feature_group}.pkl")
