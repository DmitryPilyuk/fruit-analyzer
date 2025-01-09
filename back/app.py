from typing import Annotated
import pathlib
import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
from src.model import FruitAnalyzeModel
from src.training_scripts.feature_groups import FeatureGroups


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Define server startup and shutdown logic."""
    os.mkdir(IMAGE_STORAGE)
    yield
    shutil.rmtree(IMAGE_STORAGE)
    os.rmdir(IMAGE_STORAGE)


app = FastAPI(lifespan=lifespan)


@app.post("/uploadimage/")
async def upload_image(image: Annotated[UploadFile, File()]):
    """Upload fruit image to local storage."""
    if not image:
        return error("No file sent")

    # check file extension
    image_extenstion = pathlib.Path(image.filename).suffix
    if image_extenstion not in OPENCV_SUPPORTED_IMAGE_EXTENSIONS:
        return error(
            f"Unsupported file extension! Please use one of these: {OPENCV_SUPPORTED_IMAGE_EXTENSIONS}"
        )

    image_path = IMAGE_STORAGE + image.filename

    if os.path.exists(image_path):
        os.remove(image_path)

    image_bytes = await image.read()  # Read content

    with open(image_path, "wb") as binary_file:
        binary_file.write(image_bytes)

    return {
        "file_size": len(image_bytes),
        "file_name": image.filename,
        "content_type": image.content_type,
    }


@app.get("/analyzeimage/{image_name}/{model_name}")
def analyze_image(image_name: str, model_name: str):
    image_path = IMAGE_STORAGE + image_name

    if not os.path.exists(image_path):
        return error(f'Can\'t find file "{image_path}"')

    try:
        analyze_model = convert_name_to_model(model_name)

        prediction_dict = analyze_model.get_prediction(image_path)
    except Exception as ex:
        return error(str(ex))

    return prediction_dict


def error(msg):
    return {"error_message": msg}


def convert_name_to_model(model_name: str):
    model_path = ""
    feature_groups = FeatureGroups.ALL

    if model_name == "basic_model":
        model_path = "models/main_model.pkl"

    elif model_name == "color_model":
        model_path = "models/FeatureGroups.COLOR.pkl"
        feature_groups = FeatureGroups.COLOR

    elif model_name == "leaf_model":
        model_path = "models/FeatureGroups.LEAF.pkl"
        feature_groups = FeatureGroups.LEAF

    elif model_name == "shape_model":
        model_path = "models/FeatureGroups.SHAPE.pkl"
        feature_groups = FeatureGroups.SHAPE

    elif model_name == "structure_model":
        model_path = "models/FeatureGroups.STRUCTURE.pkl"
        feature_groups = FeatureGroups.STRUCTURE

    elif model_name == "texture_model":
        model_path = "models/FeatureGroups.TEXTURE.pkl"
        feature_groups = FeatureGroups.TEXTURE
    else:
        raise Exception("Can't find such model :(")

    return FruitAnalyzeModel(model_path, feature_groups)


IMAGE_STORAGE = "images/"

OPENCV_SUPPORTED_IMAGE_EXTENSIONS = [
    ".bmp",
    ".dib",
    ".jpeg",
    ".jpg",
    ".jpe",
    ".jp2",
    ".png",
    ".webp",
    ".pbm",
    ".pgm",
    ".ppm",
    ".pxm",
    ".pnm",
    ".sr",
    ".ras",
    ".tiff",
    ".tif",
    ".exr",
    ".hdr",
    ".pic",
]
