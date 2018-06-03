import scrapy
from scrapy import Selector


class HeroesSpider(scrapy.Spider):
    name = 'heroes'
    start_urls = ['https://pro.moba.garena.co.id/heroList']

    def parse(self, response):
        for hero in response.css('.herolist-list__item'):
            href = hero.css('a.herolist-list__item-a::attr(href)').extract_first()
            yield scrapy.Request(href, callback=self.parse_hero)


    def parse_hero(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip().replace('\u2019', ' ')

        def extract_skill_name(array_number):
            inner = response.css('.hero-data__skills-item::attr(title)').extract()[array_number]
            sel = Selector(text=inner)
            skill = sel.css('.tootip-name::text').get()
            return skill

        def extract_skill_desc(array_number):
            inner = response.css('.hero-data__skills-item::attr(title)').extract()[array_number]
            sel = Selector(text=inner)
            skill = sel.css('.tootip-desc::text').get()
            return skill

        yield {
            'name': extract_with_css('.hero-data__name::text'),
            'image': extract_with_css('.hero-data__img-img-w > img::attr(src)'),
            'skill_1' : extract_skill_name(0),
            'skill_1_img' : response.css('.hero-data__skills-item > img.hero-data__skills-item-img::attr(src)').extract()[0],
            'skill_1_desc': extract_skill_desc(0),
            'skill_2' : extract_skill_name(1),
            'skill_2_img' : response.css('.hero-data__skills-item > img.hero-data__skills-item-img::attr(src)').extract()[1],
            'skill_2_desc': extract_skill_desc(1),
            'skill_3' : extract_skill_name(2),
            'skill_3_img' : response.css('.hero-data__skills-item > img.hero-data__skills-item-img::attr(src)').extract()[2],
            'skill_3_desc': extract_skill_desc(2),
            'skill_4' : extract_skill_name(3),
            'skill_4_img' : response.css('.hero-data__skills-item > img.hero-data__skills-item-img::attr(src)').extract()[3],
            'skill_4_desc': extract_skill_desc(3),
            'defend_stat' : response.css('dd.hero-data__overview-item-val::text').extract()[0],
            'attack_stat' : response.css('dd.hero-data__overview-item-val::text').extract()[1],
            'skill_stat' : response.css('dd.hero-data__overview-item-val::text').extract()[2],
            'difficulty_stat' : response.css('dd.hero-data__overview-item-val::text').extract()[3],
            'story' : extract_with_css('.catalog-entries__main::text')
        }