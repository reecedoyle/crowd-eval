# -*- coding: utf-8 -*-
import re
import MySQLdb

db = MySQLdb.connect(host="localhost", user="scraper", passwd="scraper", db="CrowdEval")
cursor = db.cursor()
cursor.execute('SELECT * FROM CloudResults')
results = cursor.fetchall()

urls = {}
for result in results:
	url = re.match('https?:\/\/(.*?)\/?$', result[3]).group(1)
	if url in urls:
		print cursor.execute('DELETE FROM CloudResults WHERE topic=%s AND rank=%s', [result[0], result[1]])
		print 'delete'
	else:
		urls[url] = 1
		snippet = ' '.join(result[4].replace('*', '').split()).lstrip().rstrip()
		print cursor.execute('UPDATE CloudResults SET snippet=%s WHERE topic=%s AND rank=%s', [snippet, result[0], result[1]])
		print 'update'
db.commit()
