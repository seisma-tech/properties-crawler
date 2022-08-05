# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    location = scrapy.Field()
    bed_num = scrapy.Field()
    bath_num = scrapy.Field()
    car_park_num = scrapy.Field()
    property_type = scrapy.Field()
    space = scrapy.Field()
    price = scrapy.Field()
    suburb_profile = scrapy.Field()

class MarketTrends(scrapy.Item):
    bed_num = scrapy.Field()
    property_type = scrapy.Field()
    median_price = scrapy.Field()
    avg_days_on_market = scrapy.Field()
    clearance_rate = scrapy.Field()
    sold_this_year = scrapy.Field()
