# -*- coding: utf-8 -*-
import scrapy
from duckduckgo.items import DuckDuckGoItem
import HTMLParser
import re


class ResultsSpider(scrapy.Spider):
	name = "duckResultsScraper"
	allowed_domains = ["duckduckgo.com"]
	start_urls = [['https://duckduckgo.com/html/?q='+'+'.join(line.split())+'+site%3Aucl.ac.uk' for line in open('/Users/reecedoyle/Documents/4th_Year/COMPM052/crowd-eval/queries.txt', 'r')][3]]

	def parse(self, response):
		#print 'hello'
		topic_no = self.getTopicNo(response.url)
		items = []  # [[title, link, snippet]]
		count = 0
		for sel in response.xpath('//*[contains(@class, "result__a")]'):
			text = sel.extract()
			items.append(DuckDuckGoItem())
			items[count]['title'] = HTMLParser.HTMLParser().unescape(re.sub('<[^<]+?>', '', text)).lstrip().rstrip()
			items[count]['link'] = re.search('href="(.*)"', text).group(1)
			items[count]['rank'] = count + 1
			items[count]['topic'] = topic_no
			count += 1
		count = 0
		print items
		for sel in response.xpath('//*[contains(@class, "result__snippet")]'):
			items[count]['snippet'] = HTMLParser.HTMLParser().unescape(re.sub('<[^<]+?>', '', sel.extract())).lstrip().rstrip()
			yield items[count]
			count += 1

	def getTopicNo(self, url):
		start_urls = ['https://duckduckgo.com/html/?q='+'+'.join(line.split())+'+site%3Aucl.ac.uk' for line in open('/Users/reecedoyle/Documents/4th_Year/COMPM052/crowd-eval/queries.txt', 'r')]
		topic_no = 0
		for start_url in start_urls:
			topic_no += 1
			if url == start_url:
				break
		return topic_no
