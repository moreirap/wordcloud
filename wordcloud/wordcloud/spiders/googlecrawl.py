# -*- coding: utf-8 -*-
import datetime
import urlparse
import socket

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader

from wordcloud.items import WordcloudItem

class WordCloudSpider(CrawlSpider):
    name = 'googlecrawl'
    allowed_domains = ['www.google.co.uk']
    base_url = 'https://www.google.co.uk/search?q=' 
    start_urls = []

    # Rules for horizontal and vertical crawling
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@id="nav"]//a[child::span/text() = "Next"]')),
        Rule(LinkExtractor(restrict_xpaths='//*[@class="r"]//a'), callback='parse_item', process_request = '_process_request')
    )

    def _build_absolute_url(self,url):
        return url

    def _process_request(self,req):
        req.meta['dont_redirect'] = True

    def __init__(self, category='', query='bill gates microsoft',*args, **kwargs):
        self.log('ENTER __init__')
        super(WordCloudSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.base_url + ''.join(query.split()).strip('+')]
        self.log('EXIT __init__')
    
    
    def parse_item(self, response):
        """ This function parses a google result page.

        @url https://www.google.co.uk/search?q=bill+gates+microsoft
        @returns items 1
        @scrapes title url html
        @scrapes project spider server date
        """

        self.log('ENTER parse_item')

        # Create the loader using the response
        l = ItemLoader(item=WordcloudItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('title', '//title/text()')
        l.add_value('url', response.url)
        #l.add_value('html', response.body)

        # Housekeeping fields
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        self.log('EXIT parse_item')

        return l.load_item()
