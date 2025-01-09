from src.training_scripts.feature_extraction import extract_features
from src.training_scripts.feature_groups import FeatureGroups
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os
from tqdm import tqdm


def load_dataset(data_dir, feature_groups: FeatureGroups):
    """Load dataset and extract features for all images."""
    features = []
    labels = []
    for label in tqdm(os.listdir(data_dir)):
        class_dir = os.path.join(data_dir, label)
        if not os.path.isdir(class_dir):
            continue
        for image_name in tqdm(os.listdir(class_dir)):
            image_path = os.path.join(class_dir, image_name)
            try:
                feature_vector = extract_features(image_path, feature_groups)
                features.append(feature_vector)
                labels.append(label)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
    return [features, labels]


def train_model(dataset_path, feature_group: FeatureGroups):
    print("Loading dataset...")
    features, labels = load_dataset(dataset_path, feature_group)
    print(f"Dataset loaded with {len(features)} samples.")

    # Encode labels
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    # Normalize features
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels_encoded, test_size=0.2, random_state=42
    )

    # Train model using Gradient Boosting
    print("Training model...")
    model = GradientBoostingClassifier()
    param_grid = {
        "learning_rate": [0.01, 0.1, 0.2],
        "max_depth": [5, 7],
        "n_estimators": [500],
    }
    grid_search = GridSearchCV(model, param_grid, cv=3, scoring="accuracy", verbose=2)
    grid_search.fit(X_train, y_train)

    # Best model
    best_model = grid_search.best_estimator_

    # Evaluate model
    print("Evaluating model...")
    y_pred = best_model.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))

    # Save label encoding for inference
    label_mapping = dict(
        zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))
    )
    print("Label Encoding:", label_mapping)

    return best_model


# add `dataset_path` parameter if labelEncoder and scaler are not saved
def infer(model, image_path, feature_group: FeatureGroups):
    # features, labels = load_dataset(dataset_path, feature_group)
    feature_vector = extract_features(image_path, feature_group)

    # * If labels encoder and scaler are not saved (provide correct paths to save the label encoder and scaler)
    # label_encoder = LabelEncoder()
    # label_encoder.fit_transform(labels)
    # joblib.dump(label_encoder, f"../labelEncoder_{feature_group}.pkl")

    # scaler = StandardScaler()
    # scaler.fit_transform(features)
    # joblib.dump(scaler, f"../scaler_{feature_group}.pkl")

    label_encoder = joblib.load(
        f"models/label_encoders/labelEncoder_{feature_group}.pkl"
    )
    scaler = joblib.load(f"models/scalers/scaler_{feature_group}.pkl")

    # Normalize features
    feature_vector = scaler.transform([feature_vector])
    predicted_label_idx = model.predict(feature_vector)[0]
    probabilities = model.predict_proba(feature_vector)[0]
    probabilities_dict = {
        label_encoder.classes_[i]: probabilities[i] for i in range(len(probabilities))
    }
    predicted_label = label_encoder.classes_[predicted_label_idx]
    return {"predicted_label": predicted_label, "probabilities": probabilities_dict}


def save_model(model, path_to_save):
    joblib.dump(model, path_to_save)
