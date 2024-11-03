from pathlib import Path 
import scrapy
from scrapy.http import Response


class QuotesSPider(scrapy.Spider):
    name = "positive_news"

    def start_requests(self):
        urls = [
            "https://www.ansa.it/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")