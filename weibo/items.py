# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'weibo'
    id = Field()
    user = Field()
    content = Field()
    forward_count = Field()
    comment_count = Field()
    like_count = Field()
    url = Field()
    posted_at = Field()


