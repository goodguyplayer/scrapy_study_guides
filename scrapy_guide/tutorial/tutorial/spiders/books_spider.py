import scrapy
from pathlib import Path
from tutorial.itemsloaders import BookItemLoader
from tutorial.items import BookItem
from scrapy.exceptions import CloseSpider


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ['books.toscrape.com']
    start_urls = [
        'https://books.toscrape.com/',
    ]
    handle_httpstatus_list = [404] # to catch 404 with callback

    def parse(self, response):

        if response.status == 404:
            raise CloseSpider('Received 404 Response')
        
        for book in response.css("article.product_pod"):
            book_item = BookItemLoader(item=BookItem(), selector=book)
            
            book_item.add_css('title', 'h3 a::attr(title)')
            book_item.add_css('rating', 'p::attr(class)', re="star-rating (.*)")
            book_item.add_css('url', 'h3 a::attr(href)')
            book_item.add_css('image_url', 'div.image_container a img::attr(src)')
            book_item.add_css('price', 'div.product_price p.price_color::text')
            yield book_item.load_item()

        next_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)