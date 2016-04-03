# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class UclPipeline(object):
	def open_spider(self, spider):
		self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
					 user="scraper",         # your username
					 passwd="scraper",  # your password
					 db="CrowdEval")        # name of the data base
		self.cursor = self.db.cursor()

	def process_item(self, item, spider):
		self.cursor.execute("INSERT INTO UCLResults (topic, rank, title, link, snippet) VALUES (%s, %s, %s, %s, %s)", [item['topic'], item['rank'], item['title'], item['link'], item['snippet']])
		self.db.commit()
		print 'writing to db...'
		return item

	def close_spider(self, spider):
		self.db.close()
