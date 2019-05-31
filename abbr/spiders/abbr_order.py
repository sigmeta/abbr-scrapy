# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup as bs
import json
from abbr.items import AbbrOrderItem

class ExampleSpider(scrapy.Spider):
    name = 'aborder'
    allowed_domains = ['www.abbreviations.com']
    with open('abs.txt',encoding='utf8') as f:
        alist=f.read().split('\n')
    start_urls = ['https://www.abbreviations.com/'+m.upper() for m in alist]

    def parse(self, response):
        item=AbbrOrderItem()
        soup = bs(response.body, 'lxml')
        item['abbr']=response.url.split('/')[-1]
        item['desc'] = []
        if not soup.find('table', class_='table tdata no-margin').tr:
            yield item
        for tr in soup.find('table', class_='table tdata no-margin').find_all('tr'):
            if tr.find_all('td')[0].text.strip().upper()==item['abbr']:
                item['desc'].append(tr.find('p', class_='desc').text.strip())
            else:
                print(tr.find_all('td')[0].text.strip().upper(),item['abbr'])
        yield item

