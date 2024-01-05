import scrapy
from whiskeyscraper.items import WhiskeyScraperItem
from scrapy.loader import ItemLoader


class WhiskeySpider(scrapy.Spider):
    name = 'whiskey'
    start_urls = ['https://www.whiskyshop.com/scotch-whisky/all?item_availability=In+Stock']

    def parse(self, response):
        for products in response.css('div.product-item-info'):
                loader = ItemLoader(item=WhiskeyScraperItem(), selector=products)

                loader.add_css('name', 'a.product-item-link')
                loader.add_css('price', 'span.price', default='N/A')
                loader.add_css('link', 'a.product-item-link::attr(href)')

                yield loader.load_item()

        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            # yield response follow
            yield response.follow(next_page, callback=self.parse)
