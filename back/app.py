from typing import Annotated
import pathlib
import os
import shutil
from contextlib import asynccontextmanager
from src.blocks.color import ColorBlock
from src.fruits import DetectedFruits, estimate_fruit_probability
from fastapi import FastAPI, File, UploadFile
import cv2


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Define server startup and shutdown logic."""
    os.mkdir(IMAGE_STORAGE)
    yield
    shutil.rmtree(IMAGE_STORAGE)


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
        "FileSize": len(image_bytes),
        "FileName": image.filename,
        "ContentType": image.content_type,
    }


@app.get("/analyzeimage/{image_name}")
def analyze_image(image_name: str):
    image_path = IMAGE_STORAGE + image_name

    if not os.path.exists(image_path):
        return error(f'Can\'t find file "{image_path}"')

    # TODO move it into a separate function instead of main.py file
    test_fruits_list = [
        DetectedFruits(Banana=True, Apple=True),
        DetectedFruits(Banana=True, Orange=True),
        DetectedFruits(Banana=True, Pineapple=True, Grapes=True),
    ]

    return estimate_fruit_probability(test_fruits_list)


def error(msg):
    return {"ErrorMessage": msg}


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
