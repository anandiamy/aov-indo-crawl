import scrapy
from scrapy import Selector


class TalentsSpider(scrapy.Spider):
    name = 'talents'
    start_urls = ['http://aov.garena.co.id/main/game/talent/']

    def parse(self, response):
        for talent in response.css('.s_deta'):
            def extract_desc(talent):
                inner = talent.css('.s_text').extract_first().replace('<br>', ' ')
                sel = Selector(text=inner)
                result = sel.css('.s_text::text').get()
                return result

            yield {
                'name': talent.css('.s_title::text').extract_first(),
                'image': talent.css('.s_icon > img::attr(src)').extract_first(),
                'desc' : extract_desc(talent)
            }
