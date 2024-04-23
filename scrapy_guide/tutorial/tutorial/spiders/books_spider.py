from pathlib import Path
from tutorial.items import BookItem

import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ['books.toscrape.com']
    start_urls = [
        'https://books.toscrape.com/',
    ]

    def parse(self, response):
        book_item = BookItem()
        for book in response.css("article.product_pod"):
            book_item['title'] = book.css('h3 a::attr(title)').extract_first()
            book_item['rating'] = book.css('p::attr(class)').extract_first().replace("star-rating ", "")
            book_item['url'] = response.urljoin(book.css('h3 a::attr(href)').extract_first())
            book_item['image_url'] = response.urljoin(book.css('div.image_container a img::attr(src)').extract_first())
            book_item['price'] = book.css('div.product_price p.price_color::text').extract_first()
            yield book_item

        next_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)