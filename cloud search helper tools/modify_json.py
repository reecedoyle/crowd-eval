#this script modifies every json generated to contain the a new field that holds the url of the html file.
# the url is made available as the first string in the content field, right up to the first end line character
import json
import pprint
count = 0
#for all jsons
for i in range(1,235):
	path = "D:\\irdm scrape\\set1\\json\\"+str(i)+".json"
	docs = json.loads(open(path, encoding="utf8").read())
	
	#for all documents in the json
	for d in docs:
		url = d['fields']['content'].split("\n",1)[0]
		#add the url field
		d['fields']['url'] = url
	
	#dump the new json to file
	with open("D:\\irdm scrape\\set1\\modified_json\\"+str(i)+".json", 'w') as outfile:
		json.dump(docs,outfile, sort_keys= True, indent =4)


