# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from .items import ChewyItem, ReviewItem


class WriteItemPipeline(object):

	def __init__(self):
		self.chewy_filename = 'chewy_cat.csv'
		self.review_filename = 'reviews.csv'

	def open_spider(self, spider):
		self.chewy_csvfile = open(self.chewy_filename, 'wb')
		self.chewy_exporter = CsvItemExporter(self.chewy_csvfile)
		self.chewy_exporter.start_exporting()
		self.review_csvfile = open(self.review_filename, 'wb')
		self.review_exporter = CsvItemExporter(self.review_csvfile)
		self.review_exporter.start_exporting()

	def close_spider(self, spider):
		self.chewy_exporter.finish_exporting()
		self.chewy_csvfile.close()
		self.review_exporter.finish_exporting()
		self.review_csvfile.close()

	def process_item(self, item, spider):
		if isinstance(item, ChewyItem):
			self.chewy_exporter.export_item(item)
		if isinstance(item, ReviewItem):
			self.review_exporter.export_item(item)
		return item