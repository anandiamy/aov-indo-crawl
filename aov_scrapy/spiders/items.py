# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector


class ItemsSpider(scrapy.Spider):
    name = 'items'
    start_urls = ['https://aov.garena.co.id/main/game/item/']

    def parse(self, response):

        def extract_item_desc():
            inner = response.css('a.J-tooltip::attr(title)').extract_first()
            sel = Selector(text=inner)
            item_desc = sel.css('.tooltip-tip::text').get()
            return item_desc

        for item in response.css('.p_box'):
            yield {
                'name': item.css('::attr(data-filter)').extract_first(),
                'image': item.css('img::attr(src)').extract_first(),
                'desc' : extract_item_desc(),
                'type' : item.css('::attr(data-tags)').extract_first().lower().replace(' ', '_'),
            }
