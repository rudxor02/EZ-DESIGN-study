import time
from typing import Any, Union

import requests
from fastapi import FastAPI, Request

app = FastAPI()


class SlowSingletonSession:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating new instance")
            cls._instance = super(SlowSingletonSession, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "session"):
            self.session = requests.Session()
            self.wiki_url = "https://en.wikipedia.org/w/api.php"
            self.cache: dict[str, Any] = {}

    def _get_params(self, query: str):
        return {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
        }

    def get(self, query: str):
        if query not in self.cache.keys():
            params = self._get_params(query)
            time.sleep(1)
            response = self.session.get(url=self.wiki_url, params=params)
            data = response.json()
            self.cache[query] = data
            return data
        return self.cache[query]


def dec(func):
    def wrapper(request: Request):
        result = func(request)
        print(request.cookies)
        print(request.headers)
        # ip print
        print(request.client.host)
        return result

    return wrapper


@app.get("/")
# @dec
def read_root(request: Request):
    query = request.query_params.get("query")
    if query is None:
        return {"error": "query is required"}
    session = SlowSingletonSession()
    return session.get(query)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
