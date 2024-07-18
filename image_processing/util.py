import glob
import cv2

import numpy as np
from pydantic import BaseModel
from datetime import datetime
import tqdm


def resize_image_in_dir(path: str, size: int = 20) -> None:
    img_paths = glob.glob(f"{path}/*.jpg")
    for img_path in img_paths:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (size, size))
        cv2.imwrite(img_path, img)
    print("resize Done")


class MaterialMeanColor(BaseModel):
    means: list
    imgs: list


def parse_materials_mean_color(path: str = "color_materials") -> MaterialMeanColor:
    means: list[np.ndarray] = []
    imgs: list[np.ndarray] = []

    img_paths = glob.glob(f"{path}/*.jpg")

    for img_path in img_paths:
        color_sum = np.array([0, 0, 0])
        img: np.ndarray = cv2.imread(img_path)
        for row in img:
            for pixcel in row:
                color_sum += pixcel
        color_mean = color_sum / (len(img) * len(img[0]))
        means.append(color_mean)
        imgs.append(img)

    return MaterialMeanColor(means=means, imgs=imgs)


def calculate_color_diff(color_1: np.ndarray, color_2: np.ndarray) -> int:
    return sum(abs(color_1 - color_2))


def search_fit_color(color: np.ndarray, color_palette: list[np.ndarray]) -> int:
    min_color_diff = 99999999
    result_index = 0
    for index, cp in enumerate(color_palette):
        color_diff = calculate_color_diff(color, cp)
        if color_diff < min_color_diff:
            min_color_diff = color_diff
            result_index = index
    return result_index


def create_mosaic_image(
    origin_img_path: str, color_palette: MaterialMeanColor, resize_rate: float = 0.4
):
    output_img = None

    origin_img = cv2.imread(origin_img_path)
    origin_img = cv2.resize(origin_img, None, fx=resize_rate, fy=resize_rate)

    for row in tqdm.tqdm(origin_img):
        output_img_row = None
        for pixel in row:
            use_palette_index = search_fit_color(pixel, color_palette.means)
            if output_img_row is None:
                output_img_row = color_palette.imgs[use_palette_index]
            else:
                output_img_row = np.concat(
                    [output_img_row, color_palette.imgs[use_palette_index]], axis=1
                )
        if output_img is None:
            output_img = output_img_row
        else:
            output_img = np.concat([output_img, output_img_row], axis=0)

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H%M%S %Z%z")
    cv2.imwrite(f"./output/{timestamp}.jpg", output_img)
