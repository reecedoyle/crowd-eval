FOR /L %%i IN (100000,1,113871) DO (
	cs-import-documents --source "D:\irdm scrape\set1\sites\url%%i.html" --output "D:\irdm scrape\set1\more json"
)	