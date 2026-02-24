import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class GeneralSpider(CrawlSpider):
    name = "general_spider"
    
    # Flexible configuration
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,
        'USER_AGENT': 'GlobalSystemBot/1.0 (+http://example.com/bot)'
    }

    def __init__(self, start_url, allowed_domain, *args, **kwargs):
        self.start_urls = [start_url]
        self.allowed_domains = [allowed_domain]
        self.rules = (
            Rule(LinkExtractor(allow=r'/'), callback='parse_item', follow=True),
        )
        super(GeneralSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        # Generic extraction logic
        yield {
            'url': response.url,
            'title': response.css('title::text').get(),
            'h1': response.css('h1::text').getall(),
            'text_content': ' '.join(response.css('p::text').getall()),
            'timestamp': datetime.now().isoformat()
        }
