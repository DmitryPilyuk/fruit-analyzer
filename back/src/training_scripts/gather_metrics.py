from model_utils import load_dataset
from feature_groups import FeatureGroups
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

dataset_path = "path/to/dataset"
le_path = "models/label_encoders/"
scaler_path = "models/scalers/"
model_path = "models/"

for feature_group in FeatureGroups:
    features, labels = load_dataset(dataset_path, feature_group)
    print(f"Dataset loaded with {len(features)} samples.")
    label_encoder = joblib.load(f"{le_path}labelEncoder_{feature_group}.pkl")
    labels_encoded = label_encoder.fit_transform(labels)
    scaler = joblib.load(f"{scaler_path}scaler_{feature_group}.pkl")
    features = scaler.fit_transform(features)
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels_encoded, test_size=0.2, random_state=42
    )
    if feature_group.value != 5:
        model = joblib.load(f"{model_path}{feature_group}.pkl")
    else:
        model = joblib.load(f"{model_path}main_model.pkl")

    y_pred = model.predict(X_test)
    print(feature_group)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))
