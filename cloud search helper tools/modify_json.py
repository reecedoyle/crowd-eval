import json
import pprint
count = 0
for i in range(1,235):
	path = "D:\\irdm scrape\\set1\\json\\"+str(i)+".json"
	docs = json.loads(open(path, encoding="utf8").read())
	
	for d in docs:
		url = d['fields']['content'].split("\n",1)[0]
		d['fields']['url'] = url
	
	with open("D:\\irdm scrape\\set1\\modified_json\\"+str(i)+".json", 'w') as outfile:
		json.dump(docs,outfile, sort_keys= True, indent =4)


