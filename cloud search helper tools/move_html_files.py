import os, sys, os.path

source_folder = "D:\\irdm scrape\\set1\\more sites\\"
dest_folder = "D:\\irdm scrape\\set1\\sites\\"

for x in range (100000,113871):
	os.rename(source_folder+"url"+str(x)+".html",dest_folder+"url"+str(x)+".html")

	