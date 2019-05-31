# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup as bs
import json
from abbr.items import VoaItem
from urllib.parse import urljoin

class ExampleSpider(scrapy.Spider):
    name = 'voabot'
    allowed_domains = ['http://www.51voa.com']
    start_urls = [f'http://www.51voa.com/VOA_Standard_{i}_archiver.html' for i in range(1,602)]
    count=0

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        lis=soup.find('div',id='list').find_all('li')
        for li in lis:
            url=urljoin(response.url,li.a['href'])
            yield scrapy.Request(url, callback=self.parse_items)

    def parse_items(self,response):
        item = VoaItem()
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
