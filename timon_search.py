#-*- coding: utf-8 -*-
import scrapy
from searchproducts.items import SearchproductsItem 
import time
from selenium import webdriver
from scrapy.selector import Selector

class SearchProducts(scrapy.Spider):
	name = 'searchTimon'

	def __init__(self):
		self.browser = webdriver.PhantomJS('/Users/minheo/phantomjs/bin/phantomjs')
		time.sleep(3)	

	def start_requests(self):
		f = open('search_Timon.txt', 'r')
		while True:
			timon_url = f.readline()
			if not timon_url: break
			yield scrapy.Request(timon_url, self.parse_Timon)
		f.close()

	def parse_Timon(self, response):
		item = SearchproductsItem() 
		self.browser.get(response.url)
		html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
		selector = Selector(text = html)
		category = selector.xpath('//*[@id="categoryName"]/text()').extract()
		title = selector.xpath('//*[@id="content"]/div[1]/div[2]/h3/text()').extract()
		url = response.url
		img = selector.xpath('//*[@id="front_image_area"]/@src').extract()
		price = ""
		for i in range(2,9):
			price += selector.xpath('//*[@id="price_info"]/div[1]/strong/span[%d]/text()' % i).extract()[0]
		count = selector.xpath('//*[@id="content"]/div[1]/div[2]/div[3]/span[1]/strong/text()').extract()
		site = 'ticketmonster'
		if (category) and (title) and (img) and (price) and (count): 
			category = category[2]
			title = title[0]
			img = img[0]
			price = price
			count = count[0]
			print category
			print title
			print img
			print price
			print count
			item['category'] = category
			item['title'] = title
			item['url'] = url
			item['img'] = img
			item['price'] = price
			item['count'] = int(count.replace(",", ""))
			item['site'] = site
			yield item
