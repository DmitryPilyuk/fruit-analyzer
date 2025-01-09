import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops
from src.training_scripts.feature_groups import FeatureGroups


# Feature extraction functions
def extract_texture_features(image):
    """
    Extract texture features using GLCM (Gray-Level Co-occurrence Matrix).
    """
    gray = np.uint8(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    gray_image = np.uint8(gray)
    distances = [1, 2, 4]  # Focused distances for capturing texture at different scales
    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    glcm = graycomatrix(
        gray_image,
        distances=distances,
        angles=angles,
        levels=256,
        symmetric=True,
        normed=True,
    )
    texture_features = []
    properties = ["contrast", "homogeneity", "energy", "correlation"]
    for prop in properties:
        values = graycoprops(glcm, prop)
        texture_features.append(np.mean(values))  # Average values for each property
    return texture_features


def extract_shape_features(image):
    """
    Extract shape features with focus on key metrics.
    """
    gray = np.uint8(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    contours, _ = cv2.findContours(
        cv2.Canny(gray, 100, 200), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contour = contours[0]
    image_shape = image.shape
    if contour is None or len(contour) == 0:
        return [0] * 8  # Return zeros if no valid contour

    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    circularity = (4 * np.pi * area) / (perimeter**2) if perimeter != 0 else 0
    bounding_rect = cv2.boundingRect(contour)
    aspect_ratio = (
        float(bounding_rect[2]) / bounding_rect[3] if bounding_rect[3] != 0 else 0
    )
    normalized_area = area / (
        image_shape[0] * image_shape[1]
    )  # Normalize by image size

    # Convexity and extent
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area if hull_area != 0 else 0
    extent = (
        area / (bounding_rect[2] * bounding_rect[3]) if bounding_rect[3] != 0 else 0
    )

    return [
        area,
        perimeter,
        circularity,
        aspect_ratio,
        normalized_area,
        hull_area,
        solidity,
        extent,
    ]


def extract_structure_features(image):
    """
    Extract structural features capturing segment distributions.
    """
    gray = np.uint8(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    contours, _ = cv2.findContours(
        cv2.Canny(gray, 100, 200), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    segment_areas = [cv2.contourArea(c) for c in contours]

    if not segment_areas:
        return [0, 0, 0, 0]  # No structures detected

    num_segments = len(segment_areas)
    mean_area = np.mean(segment_areas)
    max_area = np.max(segment_areas)
    skewness = (
        ((np.mean(segment_areas) - np.median(segment_areas)) ** 3)
        / (np.std(segment_areas) ** 3)
        if np.std(segment_areas) > 0
        else 0
    )  # Skewness of area distribution

    return [num_segments, mean_area, max_area, skewness]


def extract_leaf_features(image):
    """
    Detect and extract leaf-specific features, ensuring green regions are not misclassified as fruits.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    leaf_areas = [cv2.contourArea(c) for c in contours]

    if not leaf_areas:
        return [0, 0, 0, 0, 0]

    valid_leaves = []
    for contour in contours:
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = cv2.contourArea(contour) / hull_area if hull_area != 0 else 0
        bounding_rect = cv2.boundingRect(contour)
        aspect_ratio = (
            float(bounding_rect[2]) / bounding_rect[3] if bounding_rect[3] != 0 else 0
        )
        if 0.2 < solidity < 0.95 and aspect_ratio > 0.5:
            valid_leaves.append(contour)

    if not valid_leaves:
        return [0, 0, 0, 0, 0]

    valid_leaf_areas = [cv2.contourArea(c) for c in valid_leaves]
    num_leaves = len(valid_leaf_areas)
    total_leaf_area = np.sum(valid_leaf_areas)
    mean_leaf_area = np.mean(valid_leaf_areas)
    max_leaf_area = np.max(valid_leaf_areas)

    return [num_leaves, total_leaf_area, mean_leaf_area, max_leaf_area, len(contours)]


def extract_color_features(image):
    """
    Extract color histogram features in HSV color space.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist_h = cv2.calcHist([hsv], [0], None, [16], [0, 256]).flatten()  # Higher bins
    hist_s = cv2.calcHist([hsv], [1], None, [8], [0, 256]).flatten()
    hist_v = cv2.calcHist([hsv], [2], None, [8], [0, 256]).flatten()

    # Normalize histograms
    hist_h = hist_h / hist_h.sum()
    hist_s = hist_s / hist_s.sum()
    hist_v = hist_v / hist_v.sum()

    return np.hstack([hist_h, hist_s, hist_v])


def feature_group_to_extraction_function(feature_group: FeatureGroups):
    match feature_group.value:
        case FeatureGroups.TEXTURE.value:
            return extract_texture_features
        case FeatureGroups.STRUCTURE.value:
            return extract_structure_features
        case FeatureGroups.SHAPE.value:
            return extract_shape_features
        case FeatureGroups.LEAF.value:
            return extract_leaf_features
        case FeatureGroups.COLOR.value:
            return extract_color_features


def extract_features(image_path, feature_groups: FeatureGroups):
    """
    Extract features from the image
    """

    image = cv2.imread(image_path)
    image = cv2.resize(image, (300, 300))

    if feature_groups.value == FeatureGroups.ALL.value:
        texture_features = extract_texture_features(image)
        shape_features = extract_shape_features(image)
        structure_features = extract_structure_features(image)
        leaf_features = extract_leaf_features(image)
        color_features = extract_color_features(image)

        return np.hstack(
            [
                texture_features,
                shape_features,
                structure_features,
                leaf_features,
                color_features,
            ]
        )

    else:
        features = feature_group_to_extraction_function(feature_groups)(image)
        return np.hstack(features)
