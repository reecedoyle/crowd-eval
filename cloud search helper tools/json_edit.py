import os, sys, os.path

json_path = "D:\irdm scrape\set1\more json"

base = 234
for root,dirs, filenames in os.walk(json_path):
	for f in filenames:
		f = os.path.join(root, f) 
		#print(f[f.rfind("\\")+1:f.find(".")])
		os.rename(f,f[:f.rfind("\\")+1] + str(int(f[f.rfind("\\")+1:f.find(".")])+base)+".json")
	