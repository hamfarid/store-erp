"""
Module: universal_spider.py
Universal Spider — part of Global System v26.0.2 Diamond 32.
"""
import scrapy
import yaml
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class UniversalSpider(CrawlSpider):
    """
    Universalspider implementation.
    """
    name = "universal_spider"
    
    def __init__(self, target_name=None, *args, **kwargs):
        """
          init   implementation.
        """
        # Load config dynamically
        with open('infrastructure/scraping/config/targets.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Find target config
        self.target = next((t for t in config['targets'] if t['name'] == target_name), None)
        if not self.target:
            raise ValueError(f"Target {target_name} not found in config")

        self.start_urls = self.target['start_urls']
        self.allowed_domains = self.target['allowed_domains']
        
        # Build rules dynamically
        self.rules = tuple(
            Rule(LinkExtractor(allow=r['allow']), callback=r['callback'], follow=True)
            for r in self.target.get('rules', [])
        )
        
        super(UniversalSpider, self).__init__(*args, **kwargs)

    def parse_article(self, response):
        """
        Parse article implementation.
        """
        selectors = self.target['selectors']
        yield {
            'url': response.url,
            'title': response.css(selectors['title']).get(),
            'body': ' '.join(response.css(selectors['body']).getall()),
            'date': response.css(selectors['date']).get(),
            'source': self.target['name']
        }

    def parse_product(self, response):
        """
        Parse product implementation.
        """
        selectors = self.target['selectors']
        yield {
            'url': response.url,
            'name': response.css(selectors['name']).get().strip(),
            'price': response.css(selectors['price']).get(),
            'rating': response.css(selectors['rating']).get(),
            'source': self.target['name']
        }
