# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ChewyItem(scrapy.Item):
	product = scrapy.Field() 
	brand = scrapy.Field()
	old_price = scrapy.Field()
	new_price = scrapy.Field()
	num_reviews = scrapy.Field()
	recommand = scrapy.Field()
	rating = scrapy.Field()
	key_benefit = scrapy.Field()
	#info include weight lifestage food type etc.
	info_dict = scrapy.Field()

class ReviewItem(scrapy.Item):
	product = scrapy.Field()
	review_date = scrapy.Field()
	review_title= scrapy.Field()
	review_text = scrapy.Field()
	review_rating = scrapy.Field()
	
