import scrapy
from ..items import QuotesToScrapeItem


class QuotesToScrapeSpider(scrapy.Spider):
    name = 'quotes.toscrape'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    root_url = 'http://quotes.toscrape.com'
    item_class = QuotesToScrapeItem

    def parse(self, response, **kwargs):
        """."""

        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            item = self.item_class(quote=quote.css('span::text').get(), author=quote.css('small::text').get())
            yield item

        try:
            next_page = response.xpath('//li[@class="next"]/a')
            next_link = next_page.attrib.get('href')
            if next_link:
                yield scrapy.Request(url=self.root_url+next_link, callback=self.parse)
        except Exception as exc:
            print(exc)
