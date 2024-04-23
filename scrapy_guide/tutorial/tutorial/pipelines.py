# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from dotenv import dotenv_values
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class TutorialPipeline:
    def process_item(self, item, spider):
        return item


class PriceToUSDPipeline:
    gbpToUsdRate = 1.24 #2024-04-23 (09:03 AM)


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            floatPrice = float(adapter['price'])
            adapter['price'] = floatPrice * self.gbpToUsdRate
            return item
        
        else:
            raise DropItem(f"Missing price in {item}")
        


class DuplicatesPipeline:

    def __init__(self) -> None:
        self.names_seen = set()

    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['title'])
            return item


class SavingToMySQLPipeline(object):
    def __init__(self) -> None:
        self.create_connection()

    
    def create_connection(self):
        config = dotenv_values(".env")
        self.conn = mysql.connector.connect(
            host = config["MYSQL_HOST"],
            user = config["MYSQL_USER"],
            password = config["MYSQL_PASSWORD"],
            database = config["MYSQL_DATABASE"]
        )
        self.curr = self.conn.cursor()

    
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    

    def store_db(self, item):
        self.curr.execute("""INSERT INTO books_scrapy (title, rating, url, image_url, price) values (%s, %s, %s, %s, %s)""", 
                          (item["title"],
                          item["rating"],
                          item["url"],
                          item["image_url"],
                          item["price"]
                        ))
        self.conn.commit()

    
    def insert_one_query():
        return """INSERT INTO books_scrapy (title, rating, url, image_url, price) values (%s, %s, %s, %s, %s)"""