import asyncio

from week4.crawler import Crawler


async def main():
    wconcept_crawler = Crawler(
        name="wconcept",
        item_boxes_url="https://display.wconcept.co.kr/category/women/{category}?page={page}",
        item_box_selector="#container > div > div > div > div > section > div > div > div",
        name_selector="span > button > span.prdc-title > span.detail",
        brand_selector="span > button > span.prdc-title > span.title",
        price_selector="span > button > span.prdc-price > span.final-price > strong",
    )

    await wconcept_crawler.run(category="001001")


if __name__ == "__main__":
    asyncio.run(main())
