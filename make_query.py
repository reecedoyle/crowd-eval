import requests, json
import urllib.request, sys
import csv

#read in the topics.
with open('queries.txt') as qf:
	topics = qf.readlines()

topicNum = 0

#write to csv
with open('D:\\irdm scrape\\results.csv','w') as csvfile:
	fieldnames = ['topic', 'rank', 'title', 'link', 'snippet']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	
	# for every topic, query search engine for results
	for t in topics:
		topicNum = topicNum + 1
		print("requesting "+t)
		r = requests.get("http://search-uclirdmgroupsearch-3huyv2nm2omuy2f5kchgde7rjq.eu-west-1.cloudsearch.amazonaws.com/2013-01-01/search?q="+t+"&highlight.content={format:'text'}&size=30")
		data = r.json()
		
		#variable to hold rank
		count = 1
		
		#dictionary to weed out duplicate results
		url_dict = {}
		
		#for every doc returned
		for h in data['hits']['hit']:
			doc = h['fields']
			
			# not sure why this line is here.
			if(('title' not in doc) or ('url' not in doc)):
				continue
			url = re.match('https?:\/\/(.*?)\/?$', str(doc['url'])).group(1)
			# if duplicate detected, skip
			if(url) in url_dict):
				continue
			
			url_dict[url]=1
			
			print doc['snippet']
			#write to the csv
			#writer.writerow({'topic': str(topicNum), 'rank': str(count), 'title': doc['title'], 'link': doc['url'], 'snippet': h['highlights']["content"].replace("*","").encode('utf-8','replace')})
			
			#controlling how many results to return per query
			if count == 30:
				break
			count = count + 1
	
	