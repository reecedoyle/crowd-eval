# -*- coding: utf-8 -*-
import scrapy
import re
import HTMLParser
from ucl.items import UclItem


class UclResultsSpider(scrapy.Spider):
	name = "uclResultsScraper"
	allowed_domains = ["ucl.ac.uk"]
	start_urls = ['http://search2.ucl.ac.uk/s/search.html?query='+'+'.join(line.split())+'&collection=website-public' for line in open('/Users/reecedoyle/Documents/4th_Year/COMPM052/crowd-eval/queries.txt', 'r')]

	def parse(self, response):
		#print 'hello'
		topic_no = self.getTopicNo(response.url)
		items = []  # [[title, link, snippet]]
		count = 0
		for sel in response.xpath('//*[(@id = "fb-results")]//h3/a'):
			text = sel.extract()
			items.append(UclItem())
			items[count]['title'] = HTMLParser.HTMLParser().unescape(re.sub('<[^<]+?>', '', text)).lstrip().rstrip()
			items[count]['link'] = re.search('title="(.*)"', text).group(1)
			items[count]['rank'] = count + 1
			items[count]['topic'] = topic_no
			count += 1
		count = 0
		print items
		for sel in response.xpath('//*[contains(@class, "fb-summary")]'):
			items[count]['snippet'] = HTMLParser.HTMLParser().unescape(re.sub('<[^<]+?>', '', sel.extract())).lstrip().rstrip()
			yield items[count]
			count += 1

	def getTopicNo(self, url):
		start_urls = ['http://search2.ucl.ac.uk/s/search.html?query='+'+'.join(line.split())+'&collection=website-public' for line in open('/Users/reecedoyle/Documents/4th_Year/COMPM052/crowd-eval/queries.txt', 'r')]
		topic_no = 0
		for start_url in start_urls:
			topic_no += 1
			if url == start_url:
				break
		return topic_no
