from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

class BookItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    price_in = MapCompose(lambda x: x.split("£")[-1])
    url_in = MapCompose(lambda x: 'https://books.toscrape.com/' + x)
    image_url_in = MapCompose(lambda x: 'https://books.toscrape.com' + (x.replace("..", "")))