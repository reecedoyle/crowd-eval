FOR /L %%i IN (2,1,234) DO (
	aws cloudsearchdomain --endpoint-url http://doc-uclirdmgroupsearch-3huyv2nm2omuy2f5kchgde7rjq.eu-west-1.cloudsearch.amazonaws.com upload-documents --content-type application/json --documents "D:\irdm scrape\set1\modified_json\%%i.json"
)	

