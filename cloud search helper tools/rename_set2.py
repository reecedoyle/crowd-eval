import os, sys, os.path

set1 = 'D:\irdm scrape\set1\sites'
base = len(os.listdir(set1))
set2 = "D:\irdm scrape\set2\sites"
files = os.listdir(set2)

for root,dirs, filenames in os.walk(set2):
	for f in filenames:
		f = os.path.join(root, f) 
		os.rename(f,f[:f.find("url")+3]+str(int(f[len(set2)+4:f.find('.')])+base)+".html")
	