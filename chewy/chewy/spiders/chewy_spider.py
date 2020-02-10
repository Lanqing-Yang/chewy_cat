from scrapy import Spider, Request
from chewy.items import ChewyItem, ReviewItem
import re

class ChewySpider(Spider):
	name = 'chewy_spider'
	allowed_domains = ['www.chewy.com']
	start_urls = ['https://www.chewy.com/s?rh=c%3A325%2Cc%3A387&page=1']
	print("#"*50)

	def parse(self, response):
		#find number of pages
		text = response.xpath('//div[@class="results-header__title"]/p/text()').extract_first()
		_, per_page, total = map(lambda x: int(x), re.findall('\d+', text))
		number_pages = total // per_page
		result_urls = ['https://www.chewy.com/s?rh=c%3A325%2Cc%3A387&page={}'.format(x) for x in range(1, number_pages+1)]

		for url in result_urls:
			yield Request(url=url, callback=self.parse_result_page)

	def parse_result_page(self, response):
		detailed_urls = response.xpath('//article[@class="product-holder js-tracked-product  cw-card cw-card-hover"]/a/@href').extract()
		for url in detailed_urls:
			yield Request(url='https://www.chewy.com/' + url, callback=self.parse_detailed_page)

	def parse_detailed_page(self, response):
		product = response.xpath('//div[@id="product-title"]/h1/text()').extract_first().strip()
		brand = response.xpath('//div[@id="product-subtitle"]/a/span/text()').extract_first()
		try:
			old_price = float(response.xpath('//li[@class="list-price"]/p/text()').extract()[1].strip().split('$')[1])
		except:
			old_price = 0
		new_price = float(response.xpath('//li[@class="our-price"]/p/span/text()').extract_first().strip().split('$')[1])
		recommand = int(response.xpath('//span[@class="progress-radial__text--percent"]/text()').extract_first())
		rating = float(response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first())
		key_benefit = response.xpath('//section[@class="descriptions__content cw-tabs__content--left"]/ul/li/text()').extract()
		try:
			num_reviews = int(re.findall('\d+', response.xpath('//div[@class="ugc ugc-head"]/span').extract_first())[0])
		except: 
			num_reviews = 0

		#information about weight, lifestange, foodtype, etc
		attributes = response.xpath('//ul[@class="attributes"]//li')
		info_dict = dict()
		try:
			for attribute in attributes:
				key = ''.join(attribute.xpath('./div[@class="title"]/text()').extract()).strip()
				value = ''.join(attribute.xpath('./div[contains(@class,"value")]//text()').extract()).strip()
				info_dict[key] = value
				#info_dict[key] = value
		except:
			info_dict = 0 #0

		item = ChewyItem()
		item['old_price'] = old_price 
		item['product'] = product
		item['num_reviews'] = num_reviews
		item['new_price'] = new_price
		item['brand'] = brand
		item['recommand'] = recommand
		item['rating'] = rating
		item['key_benefit'] = key_benefit
		item['info_dict'] = info_dict
		yield item

		#construct urls:
		review_page = response.xpath('//footer[@class="ugc-list__footer js-read-all"]/a/@href').extract()[0][:-1]
		review_urls= ['https://www.chewy.com' + review_page + str(x) for x in range(1, num_reviews//10+1)]
		for url in review_urls:
			yield Request(url=url, meta={'product': product}, callback=self.parse_review_page)

	def parse_review_page(self, response):
		product = response.meta['product']

		reviews = response.xpath('//li[@class="js-content"]')
		response.xpath('//li[@class="js-content"]//span[@class="ugc-list__review__display"]/text()').extract()
		
		response.xpath('//ul[@class="attributes"]/li')
		for review in reviews:
			review_date  = review.xpath('.//span/@content').extract()[0]
			review_title = review.xpath('.//h3/text()').extract_first()
			review_text = review.xpath('.//span[@class="ugc-list__review__display"]/text()').extract_first()
			try:
				review_rating = int(review.xpath('.//@alt').extract_first().split()[0])
			except:
				review_rating = 0

			item = ReviewItem()
			item['product'] = product
			item['review_date'] = review_date
			item['review_title'] = review_title
			item['review_text'] = review_text
			item['review_rating'] = review_rating

		yield item
		


		


