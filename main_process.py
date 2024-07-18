import cv2
from scryping.image_crawler import scrape_img
from image_processing import util


def create_image(
    material_word: str,
    target_word: str,
    material_max_nums: int = 40,
    material_img_size: int = 40,
    target_resize_rate: float = 0.1,
) -> None:
    print(f"{material_word}でできた、{target_word}を生成します")
    print("\nImage collecting ...")
    scrape_img(keyword=material_word, max_num=material_max_nums, path="color_materials")
    scrape_img(keyword=target_word, max_num=1, path="convert_images")
    print(" Image collection is complete! ")
    util.resize_image_in_dir("color_materials", size=material_img_size)
    print("\n\nGenerating image ...")
    color_palette: util.MaterialMeanColor = util.parse_materials_mean_color()
    util.create_mosaic_image(
        "convert_images/000001.jpg",
        color_palette=color_palette,
        resize_rate=target_resize_rate,
    )
    print("\nDone!")
