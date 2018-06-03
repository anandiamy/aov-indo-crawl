# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector


class ArcanasSpider(scrapy.Spider):
    name = 'arcanas'
    start_urls = ['http://aov.garena.co.id/main/game/arcana/']

    def parse(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        def extract_arcana_desc(arcana):
            inner = arcana.css('a.J-tooltip::attr(title)').extract_first()
            sel = Selector(text=inner)
            result = sel.css('.tooltip-desc::text').get()
            return result

        for arcana in response.css('.k_box'):
            yield {
                'name': arcana.css('::attr(data-filter)').extract_first(),
                'image': extract_with_css('.k_b_pic img::attr(src)'),
                'desc': extract_arcana_desc(arcana),
                'level': arcana.css('::attr(data-tags)').extract_first().lower().replace(' ', '_').split(',')[-1],
                'type': arcana.css('::attr(data-tags)').extract_first().lower().replace(' ', '_').split(',')[:-1],
            }

