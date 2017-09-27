#-*- coding: utf-8 -*-
import scrapy
from searchproducts.items import SearchproductsItem 
import time
from selenium import webdriver
from scrapy.selector import Selector

class SearchProducts(scrapy.Spider):
	name = 'searchAuction'

	def __init__(self):
		self.browser = webdriver.PhantomJS('/Users/minheo/phantomjs/bin/phantomjs')
		time.sleep(3)	

	def start_requests(self):
		f = open('search_auction.txt', 'r')
		while True:
			auction_url = f.readline()
			if not auction_url: break
			yield scrapy.Request(auction_url, self.parse_auction)
		f.close()

	def parse_auction(self, response):
		item = SearchproductsItem() 
		self.browser.get(response.url)
		html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
		selector = Selector(text = html)
		category = selector.xpath('//*[@id="locbar"]/div/div[1]/div[2]/a/text()').extract()
		title = selector.xpath('//*[@id="frmMain"]/h1/text()').extract()
		url = response.url
		img = selector.xpath('//*[@id="content"]/div[2]/div[1]/div/ul/li/a/img/@src').extract()
		price = selector.xpath('//*[@id="frmMain"]/div[3]/div[1]/div/span/strong/text()').extract()
		count = selector.xpath('//*[@id="frmMain"]/div[2]/p[2]/text()').extract()
		site = 'auction'
		if (category) and (title) and (img) and (price) and (count): 
			category = category[0]
			title = title[0]
			img = img[0]
			price = price[0]
			count = count[0].split(" ")[1]
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
