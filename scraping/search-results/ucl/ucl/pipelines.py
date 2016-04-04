# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class UclPipeline(object):
	def open_spider(self, spider):
		try:
			self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
						 user="scraper",         # your username
						 passwd="scraper",  # your password
						 db="CrowdEval")        # name of the data base
			self.cursor = self.db.cursor()
			self.csv = False
		except Exception:
			self.csv = True  # write to csv because no database
			self.filename = "scraped.csv"

	def process_item(self, item, spider):
		if self.csv:
			with open(self.filename, 'a') as f:
				f.write('\t'.join([str(item['topic']), str(item['rank']), item['title'].encode('utf-8'), item['link'].encode('utf-8'), item['snippet'].encode('utf-8')])+'\n')
				print 'writing to csv...'
		else:
			self.cursor.execute("INSERT INTO UCLResults (topic, rank, title, link, snippet) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=%s, link=%s, snippet=%s", [item['topic'], item['rank'], item['title'], item['link'], item['snippet'], item['title'], item['link'], item['snippet']])
			self.db.commit()
			print 'writing to db...'
		return item

	def close_spider(self, spider):
		if not self.csv:
			self.db.close()
