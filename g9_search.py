#-*- coding: utf-8 -*-
import scrapy
from searchproducts.items import SearchproductsItem 
import time
from selenium import webdriver
from scrapy.selector import Selector

class SearchProducts(scrapy.Spider):
	name = 'searchG9'

	def __init__(self):
		self.browser = webdriver.PhantomJS('/Users/minheo/phantomjs/bin/phantomjs')
		time.sleep(3)	

	def start_requests(self):
		f = open('search_g9.txt', 'r')
		while True:
			g9_url = f.readline()
			if not g9_url: break
			yield scrapy.Request(g9_url[:-1], self.parse_G9)
		f.close()

	def parse_G9(self, response):
		item = SearchproductsItem() 
		self.browser.get(response.url)
		html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
		selector = Selector(text = html)
		category = selector.xpath('//*[@id="container"]/div[1]/div[1]/div[3]/a/text()').extract()
		title = selector.xpath('//*[@id="subjText4"]/text()').extract()
		url = response.url
		img = selector.xpath('//*[@id="goodsImage"]/@src').extract()
		price = selector.xpath('//*[@id="sDPrice2"]/text()').extract()
		count = selector.xpath('//*[@id="spOrderQty2"]/text()').extract()
		site = 'g9'
		if (category) and (title) and (img) and (price) and (count): 
			category = category[0]
			title = title[0]
			img = img[0]
			price = price[0]
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
