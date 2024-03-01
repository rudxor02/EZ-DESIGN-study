import asyncio

from week4.crawler import Crawler


async def main():
    wconcept_crawler = Crawler(
        name="musinsa",
        item_boxes_url="https://www.musinsa.com/categories/item/{category}?d_cat_cd={category}&brand=&list_kind=small&sort=pop_category&sub_sort=&page={page}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure=",
        item_box_selector="#searchList > li.li_box",
        name_selector="div.li_inner > div.article_info > p.list_info > a",
        brand_selector="div.li_inner > div.article_info > p.item_title > a",
        price_selector="div.li_inner > div.article_info > p.price",
    )

    await wconcept_crawler.run(category="007001")


if __name__ == "__main__":
    asyncio.run(main())
