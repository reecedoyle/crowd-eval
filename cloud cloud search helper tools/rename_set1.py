import os, sys, os.path

set1 = 'D:\irdm scrape\set1\sites'
base = 0

for root,dirs, filenames in os.walk(set1):
	for f in filenames:
		f = os.path.join(root, f) 
		os.rename(f,f[:f.find("url")+3]+str(base)+".html")
		base = base + 1
	