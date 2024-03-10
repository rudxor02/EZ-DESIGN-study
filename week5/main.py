import asyncio
import datetime
import logging
import threading

import psutil
import schedule
from dash import Dash, Input, Output, callback, dcc, html

from week5.metric import MetricManager, Period

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
logger = logging.getLogger(__name__)
cpu_manager = MetricManager(name="cpu", path="cpu.pkl")
memory_manager = MetricManager(name="memory", path="memory.pkl")
disk_manager = MetricManager(name="disk", path="disk.pkl")


@schedule.repeat(schedule.every(10).seconds)
def collect_data():
    print(datetime.datetime.now())
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    cpu_manager.on_collect(cpu)
    memory_manager.on_collect(memory)
    disk_manager.on_collect(disk)


async def job():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children="Local Computer Dashboard", style={"textAlign": "center"}),
        dcc.Dropdown(["15min", "1h", "3h", "1d"], "15min", id="period-dropdown"),
        dcc.Graph(id="cpu"),
        dcc.Graph(id="memory"),
        dcc.Graph(id="disk"),
        dcc.Interval(id="interval-component", interval=5 * 1000, n_intervals=0),
    ]
)


@callback(
    Output("cpu", "figure"),
    Output("memory", "figure"),
    Output("disk", "figure"),
    Input("interval-component", "n_intervals"),
    Input("period-dropdown", "value"),
)
def update_graph(n_intervals: int, period: Period):
    return (
        cpu_manager.plot(period=period),
        memory_manager.plot(period=period),
        disk_manager.plot(period=period),
    )


if __name__ == "__main__":
    loop.create_task(job())
    thread = threading.Thread(target=loop.run_forever)
    thread.start()
    app.run()
