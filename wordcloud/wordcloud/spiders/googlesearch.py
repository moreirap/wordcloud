# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import Spider
from lxml.html.clean import Cleaner

from wordcloud.items import WordcloudItem
from wordcloud.sanitizeHtml import cleanInput, plaintext, removeKnownSections


class WordCloudSpider(Spider):
    name = 'googlesearch'
    base_url = 'https://www.google.co.uk/search?q='
    start_urls = []
    beautifulsoup_parser = "lxml"

    def parse(self, response):
        # Process all google results
        for result in response.xpath('//h3[@class="r"]//a'):
            rel_url = result.xpath('./@href').extract_first()
            target_page = response.urljoin(rel_url)
            
            # Ignore google result links to image, news and books (TODO: Find a better way to manage this)
            if not str(rel_url).startswith('/search') and not str(rel_url).startswith('https://books.google'):
                request = scrapy.Request(target_page, callback=self.parse_html)
                request.meta['title'] = result.xpath('./text()').extract()
                yield request

        # Get next page results
        next_page = response.xpath('//*[@id="nav"]//a[child::span/text() = "Next"]').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            request = scrapy.Request(next_page, callback=self.parse)
            yield request

    # Proces individual result page
    def parse_html(self, response):
        # Clean HTML of unwanted tags (scripts, javascript, comments, style, etc)
        html = Cleaner().clean_html(response.body)
        # Removes known sections of websites (e.g. sidebars, footers, etc)
        html = removeKnownSections(html)
        # Convert to text
        plainText = plaintext(html)
        # strip newlines and extra characters
        cleanedHtml = ' '.join(cleanInput(plainText))
        # Return object representing parsed result
        yield WordcloudItem({
            'title': response.meta['title'],
            'url':  response.url,
            'html': cleanedHtml,
        })

    def __init__(self, category='', query='bill gates microsoft', *args, **kwargs):
        super(WordCloudSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.base_url + '+'.join(query.split())]
        
