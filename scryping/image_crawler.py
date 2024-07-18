from icrawler.builtin import BingImageCrawler


def scrape_img(keyword: str, max_num: int, path: str) -> None:
    crawler = BingImageCrawler(
        downloader_threads=4, storage={"root_dir": path}, log_level="CRITICAL"
    )
    crawler.crawl(keyword=keyword, max_num=max_num)
