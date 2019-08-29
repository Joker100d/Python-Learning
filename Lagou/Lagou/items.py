# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, MapCompose


class LagouItemLoader(ItemLoader):
    # 自定义 itemloader
    default_output_processor = TakeFirst()


def set_empty(value):
    if value:
        return value
    else:
        return 'None'


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position_name = scrapy.Field(input_processor=Join())

    exp_lvl = scrapy.Field(input_processor=Join())

    edu_lvl = scrapy.Field(input_processor=Join())

    position_type = scrapy.Field(input_processor=Join())

    position_id = scrapy.Field(input_processor=Join())

    position_url = scrapy.Field(input_processor=Join())

    finance_stage = scrapy.Field(input_processor=Join())

    industry_field = scrapy.Field(input_processor=Join())

    company_name = scrapy.Field(input_processor=Join())

    work_city = scrapy.Field(input_processor=Join())

    salary = scrapy.Field(input_processor=Join())

    position_advantage = scrapy.Field(input_processor=Join())

    publish_date = scrapy.Field(input_processor=Join())

    company_attr = scrapy.Field(input_processor=Join())

    skill_label = scrapy.Field(input_processor=Join())
