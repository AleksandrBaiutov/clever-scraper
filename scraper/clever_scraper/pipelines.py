# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Books
import config


class CleverScraperPipeline:
    def process_item(self, item, spider):
        return item

class SavingToPostgres(object):
    def process_item(self, item, spider):
    	engine = create_engine(config.DATABASE_CONNECTION_URI)
    	Session = sessionmaker(bind=engine)
    	session = Session()
    	session.add(Books(ISBN=item["ISBN"], name=item["name"],
						  price=item["price"], discount=item["discount"],
						  author=item["author"], min_age=item["min_age"],
						  rating=item["rating"], review_number=item["review_number"],
						  available=item["available"], link=item["link"]))
    	session.commit()
    	session.close()
    	return item
