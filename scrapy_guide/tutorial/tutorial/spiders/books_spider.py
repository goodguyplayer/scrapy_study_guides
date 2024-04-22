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
                'title': book.css('h3 a::attr(title)').extract_first(),
                'rating': book.css('p::attr(class)').extract_first(),
                'url': response.urljoin(book.css('h3 a::attr(href)').extract_first()),
                'image_url' : response.urljoin(book.css('div.image_container a img::attr(src)').extract_first()),
                'price' : book.css('div.product_price p.price_color::text').extract_first(),
                #'is_instock' : "",
            }
        next_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)