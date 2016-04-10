# -*- coding: utf-8 -*-
import re
import MySQLdb

db = MySQLdb.connect(host="localhost", user="scraper", passwd="scraper", db="CrowdEval")
cursor = db.cursor()
cursor.execute('SELECT * FROM CloudResults')
results = cursor.fetchall()
topic = 0
rank = 1
for result in results:
	if topic < int(result[0]):
		topic = int(result[0])
		rank = 1
	print cursor.execute('UPDATE CloudResults SET rank=%s WHERE topic=%s AND rank=%s', [rank, result[0], result[1]])
	rank += 1
db.commit()
