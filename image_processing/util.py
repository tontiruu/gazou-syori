import glob
from PIL import Image
import cv2


def resize_image_in_dir(path: str, size: int = 20) -> None:
    img_paths = glob.glob(f"{path}/*.jpg")
    for index, img_path in enumerate(img_paths):
        img = cv2.imread(img_path)
        img = cv2.resize(img, (size, size))
        cv2.imwrite(f"{path}/{index}.jpg", img)
    print("resize Done")


def get_materials_mean_color(path: str = "color_materials") -> None:
    img_paths = glob.glob(f"{path}/*.jpg")
    for index, img_path in enumerate(img_paths):
        img = cv2.imread(img_path)
