import asyncio
import logging
import os
import pickle
from datetime import datetime
from typing import Literal, OrderedDict

import pandas as pd
import plotly.express as px

Period = Literal["15min", "1h", "3h", "1d"]
loop = asyncio.get_event_loop()
logger = logging.getLogger(__name__)


class MetricManager:
    def __init__(self, name: str, path: str, threshold: float = 60.0):
        self.name = name
        self.path = path
        self.threshold = threshold
        if os.path.exists(path):
            with open(path, "rb") as f:
                self.data_dict = pickle.load(f)
        else:
            self.data_dict: OrderedDict[datetime, float] = OrderedDict()

    async def save(self, value: float):
        current_time = datetime.now()
        current_time = current_time.replace(microsecond=0).replace(
            second=current_time.second // 10 * 10
        )
        self.data_dict[current_time] = value
        with open(self.path, "wb") as f:
            pickle.dump(self.data_dict, f)

    async def log_to_stdout(self, value: float):
        if value > self.threshold:
            print(f"High {self.name} usage: {value}")

    async def log_to_file(self, value: float):
        if value > self.threshold:
            with open(f"{self.name}.log", "a") as f:
                f.write(f"{datetime.now()}: High {self.name} usage: {value}\n")

    def on_collect(self, value: float):
        loop.create_task(self.save(value))
        loop.create_task(self.log_to_stdout(value))
        loop.create_task(self.log_to_file(value))

    def get_empty_data_dict(self, period: Period) -> OrderedDict[datetime, float]:
        period_in_seconds = {
            "15min": 15 * 60,
            "1h": 60 * 60,
            "3h": 3 * 60 * 60,
            "1d": 24 * 60 * 60,
        }[period]
        current_time = datetime.now()
        current_time = current_time.replace(microsecond=0).replace(
            second=current_time.second // 10 * 10
        )
        data_dict: OrderedDict[datetime, float] = OrderedDict()
        for i in range(0, period_in_seconds, 10):
            data_dict[current_time - pd.Timedelta(seconds=i)] = None
        return data_dict

    def plot(self, period: Period):
        data_dict = self.get_empty_data_dict(period=period)
        data_dict.update(self.data_dict)

        items = data_dict.items()

        ordered_items = sorted(items, key=lambda x: x[0])

        return px.line(
            pd.DataFrame(ordered_items, columns=["time", self.name]),
            x="time",
            y=self.name,
            title=f"{self.name} usage in the last {period}",
            range_y=[0, 100],
        )
