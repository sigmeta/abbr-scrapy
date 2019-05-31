# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.pipelines.files import FilesPipeline

class AbbrPipeline(object):
    def process_item(self, item, spider):

        return item


class VoaPipeline(FilesPipeline):
    def process_item(self, item, spider):

        return item
