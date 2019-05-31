# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup as bs
import json
from abbr.items import AbbrItem

class ExampleSpider(scrapy.Spider):
    name = 'ab'
    allowed_domains = ['www.abbreviations.com']
    start_urls = ['https://www.abbreviations.com/abbreviations/'+m for m in ['0'+c for c in [chr(ord('A')+i) for i in range(26)]]+[chr(ord('A')+i) for i in range(26)]]

    def parse(self, response):
        item=AbbrItem()
        soup = bs(response.body, 'lxml')
        if not soup.find('table', class_='tdata').tr:
            return
        for tr in soup.find('table', class_='tdata').find_all('tr'):
            item['abbr'] = tr.find_all('td')[0].text.strip()
            item['desc'] = tr.find('p', class_='desc').text.strip()
            if tr.find('p', class_='path'):
                item['classes'] = [a.text.strip() for a in tr.find('p', class_='path').find_all('a')]
            else:
                item['classes'] = []

            yield item
        if soup.find('div', class_='pager'):
            pages = int(soup.find('div', class_='pager').find_all('a')[-2].text.strip())
            for page in range(2, pages + 1):
                yield scrapy.Request(response.url+ '/' + str(page), callback=self.parse_items)

    def parse_items(self,response):
        item = AbbrItem()
        soup = bs(response.body, 'lxml')
        if not soup.find('table', class_='tdata').tr:
            return
        for tr in soup.find('table', class_='tdata').find_all('tr'):
            item['abbr'] = tr.find_all('td')[0].text.strip()
            item['desc'] = tr.find('p', class_='desc').text.strip()
            if tr.find('p', class_='path'):
                item['classes'] = [a.text.strip() for a in tr.find('p', class_='path').find_all('a')]
            else:
                item['classes'] = []

            yield item
