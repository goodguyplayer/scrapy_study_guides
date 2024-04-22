from pathlib import Path

import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ['books.toscrape.com']
    start_urls = [
        'https://books.toscrape.com/',
    ]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            yield {
                'title': book.css('h3 a').attrib['title'],
                'rating': book.css('p').attrib['class'],
            }