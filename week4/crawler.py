import asyncio
from typing import Any, AsyncGenerator

import pandas as pd
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


class Crawler(BaseModel):
    name: str
    item_boxes_url: str
    item_box_selector: str
    name_selector: str
    brand_selector: str
    price_selector: str

    items: list[dict[str, Any]] = []

    def get_item_boxes_url(self, category: str, page: int) -> str:
        return self.item_boxes_url.format(page=page, category=category)

    async def item_box_iterator(
        self, category: str, page: int
    ) -> AsyncGenerator[Tag, None]:
        driver.get(self.get_item_boxes_url(category=category, page=page))
        await asyncio.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        while len((item_boxes := soup.select(self.item_box_selector))) > 0:
            for item_box in item_boxes:
                yield item_box
            page += 1
            print(f"fetching page {page}...")
            driver.get(self.get_item_boxes_url(category=category, page=page))
            await asyncio.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            item_boxes = soup.select(self.item_box_selector)

    async def run(self, category: str = "012026", page: int = 1):
        try:
            async for item_box in self.item_box_iterator(category=category, page=page):
                name = item_box.select_one(self.name_selector).text.strip()
                brand = item_box.select_one(self.brand_selector).text.strip()
                price = (
                    item_box.select_one(self.price_selector)
                    .text.strip("\n ")
                    .split("\n")[-1]
                    .strip()
                )
                self.items.append(
                    {
                        "name": name,
                        "brand": brand,
                        "price": price,
                    }
                )
            print("Saving...")
        except Exception as e:
            print(f"{e}\nSaving...")
        finally:
            df = pd.DataFrame(self.items)
            df.to_csv(f"{self.name}_{category}.csv", index=False)
