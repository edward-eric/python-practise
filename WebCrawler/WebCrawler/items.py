# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ProductItem(Item):
    sku = Field()
    title = Field()
    href = Field()
    price = Field()
    image = Field()
    evaluate = Field()
    reputation = Field()
    
