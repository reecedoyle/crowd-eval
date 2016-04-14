import MySQLdb

db = MySQLdb.connect(host="localhost", user="scraper", passwd="scraper", db="CrowdEval")
cursor = db.cursor()
cursor.execute("SELECT topic, max(credit) FROM LastFeedback GROUP BY topic")
maxCredits = cursor.fetchall()
#print maxCredits
winners = {}
rankers = {}
for (topic, credit) in maxCredits:
	cursor.execute("SELECT source FROM LastFeedback WHERE topic = %s AND credit = %s", [topic, credit])
	winners[int(topic)] = [x for xs in cursor.fetchall() for x in xs]
	print winners[topic]
	for ranker in winners[topic]:
		if ranker in rankers:
			rankers[ranker] += 1
		else:
			rankers[ranker] = 1
print len(winners)
for ranker in rankers:
	print "{0}: {1}".format(ranker, rankers[ranker]/31.0)
