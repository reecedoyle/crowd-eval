import os, sys, os.path
#the html files were received in two batches.
#thus the html files were also converted to json in 2 batches.
#conversion tool names its json files starting with 1.json, 2.json.. etc
#After conversion of the second batch,there are now 2 sets of jsons start withing 1.json, 2.json..
#this script renames the second batch by adding a base offset calculated from the size of the first batch

json_path = "D:\irdm scrape\set1\more json"

base = 234
for root,dirs, filenames in os.walk(json_path):
	for f in filenames:
		f = os.path.join(root, f) 
		os.rename(f,f[:f.rfind("\\")+1] + str(int(f[f.rfind("\\")+1:f.find(".")])+base)+".json")
	