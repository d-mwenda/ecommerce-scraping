"""
Scrap all products on jumia
"""
import scrapy

import logging

class JumiaAllProductsSpider(scrapy.Spider):
    name = "jumia-all-products"
    start_urls = [
        "https://www.jumia.co.ke"
    ]
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0.3,
        'AUTOTHROTTLE_ENABLED': False,
        'RANDOMIZE_DOWNLOAD_DELAY': False
    }

    logger = logging.getLogger("jumia-all-products")

    def parse(self, response):
        """
        Extract urls of categories from Jumia's navigation menu and
        follow the urls. Pass the responses to a different callback
        method that will process crawling of the categories.
        """
        for category_url in response.css("div.flyout a::attr(href)").getall():
            self.logger.debug(f"{category_url}")
            category_url = response.urljoin(category_url)
            self.logger.debug(f"url to follow is {category_url}")
            yield response.follow(category_url, self.parse_categories)
    
    def parse_categories(self, response):
        """
        For each category, follow the links of the products in the
        product catalogue. Go to the next page until the last page
        of the catalogue.
        """
        self.logger.debug(f"parsing category at {response.url}")
        for category_url in response.css("section.-fh div.-paxs article.prd a::attr(href)").getall():
            category_url = response.urljoin(category_url)
            self.logger.debug(f"category page url to follow is {category_url}")
            yield response.follow(category_url, self.parse_products)
        
        next_page = response.css("a.pg::attr(href)").getall()[-2]
        if next_page is not None:
            self.logger.debug(f"We have a next page!!!! {next_page}")
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, self.parse_categories)
    
    def parse_products(self, response):
        self.logger.debug(f"parsing product at {response.url}")
        product_container = response.css("main.-pvs")
        yield {
            "name": product_container.css("h1.-pts::text").get(),
            "price": product_container.css("span.-fs24[data-price]::text").get(),
        }