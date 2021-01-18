import scrapy


class PhoneScrapper(scrapy.Spider):

    name = 'phone_hunter'

    start_urls = ['https://www.jumia.co.ke/phones-tablets/']

    def parse(self, response):
        pass
