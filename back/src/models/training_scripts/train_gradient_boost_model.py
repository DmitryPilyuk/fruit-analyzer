from model_utils import train_model, save_model
from feature_groups import FeatureGroups

# train the model
DATA_DIR = "/home/alex/dev/uni/dataset_v2"
model = train_model(DATA_DIR, FeatureGroups.ALL)

# save the model
PATH_TO_SAVE = "../main_model"
save_model(model, PATH_TO_SAVE)
