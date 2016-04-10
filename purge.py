# -*- coding: utf-8 -*-
import re
import HTMLParser
import csv
import MySQLdb
import codecs

def remove_non_ascii_2(text):
	return re.sub(r'[^\x00-\x7F]',' ', text)

db = MySQLdb.connect(host="localhost", user="scraper", passwd="scraper", db="CrowdEval")
cursor = db.cursor()

data = []
urls = {}

with open('cloud-raw.csv', 'rb') as fin, codecs.open('cloud-parsed.csv', 'wb', encoding='utf-8') as fout:
	reader = csv.reader(fin, delimiter=',')
	writer = csv.writer(fout)
	count = 0
	for row in reader:
		count += 1
		#print row[:-1] + [' '.join(HTMLParser.HTMLParser().unescape(row[-1][2:-1]).split())]
		#print unicode(' '.join(HTMLParser.HTMLParser().unescape(row[-1][2:-1]).split()).replace('\\\\', '\\'), errors='replace').encode('utf-8')
		#snip = unicode(' '.join(HTMLParser.HTMLParser().unescape(row[-1][2:-1]).split()).replace('\\\\', '\\').decode('string_escape'),errors='replace')
		snip = ' '.join(HTMLParser.HTMLParser().unescape(str(row[-1][2:-1])).split()).replace('\\\\', '\\').decode('string_escape').decode('iso-8859-1').encode('utf8')
		#snip = ' '.join(HTMLParser.HTMLParser().unescape(row[-1][2:-1]).split()).replace('\\\\', '\\').decode('string_escape')
		if count == 1:
			continue
		url = re.match('https?:\/\/(.*?)\/?$', row[3]).group(1)
		if not url in urls:
			urls[url] = 1
			#writer.writerow(row[:-1]+[snip])
			item = {
				'topic':str(row[0]),
				'rank':str(row[1]),
				'title':str(row[2]).replace('\\\\', '\\').decode('string_escape').decode('iso-8859-1').encode('utf8'),
				'link':str(row[3]),
				'snippet':snip,
			}
			print item['title']
			cursor.execute("INSERT INTO CloudResults (topic, rank, title, link, snippet) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=%s, link=%s, snippet=%s", [item['topic'], item['rank'], item['title'], item['link'], item['snippet'], item['title'], item['link'], item['snippet']])
print len(urls)
