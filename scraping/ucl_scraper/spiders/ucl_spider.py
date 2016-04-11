import scrapy
import lxml
import threading
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner
from scrapy.http import HtmlResponse
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor

class UclCopySpider(scrapy.contrib.spiders.CrawlSpider):

    # Track parsed items
    lock = threading.Lock()
    parsed = {}

    # Setup html cleaner to remove js and css
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    cleaner.page_structure = False

    # Store a counter of files parsed to save a unique filename
    counter = 0
    name = "ucl"

    # Define the allowed domains for crawling
    allowed_domains = ["advancedteaching.cs.ucl.ac.uk",
     "blogs.ucl.ac.uk",
     "busics.cs.ucl.ac.uk",
     "ccs.chem.ucl.ac.uk",
     "crest.cs.ucl.ac.uk",
     "crf.casa.ucl.ac.uk",
     "discovery.ucl.ac.uk",
     "geometry.cs.ucl.ac.uk",
     "haig.cs.ucl.ac.uk",
     "iris.ucl.ac.uk",
     "is.cs.ucl.ac.uk",
     "mediafutures.cs.ucl.ac.uk",
     "nrg.cs.ucl.ac.uk",
     "onlinestore.ucl.ac.uk",
     "pplv.cs.ucl.ac.uk",
     "readinglists.ucl.ac.uk",
     "reality.cs.ucl.ac.uk",
     "sec.cs.ucl.ac.uk",
     "vecg.cs.ucl.ac.uk",
     "vis.cs.ucl.ac.uk",
     "web4.cs.ucl.ac.uk",
     "www-mice.cs.ucl.ac.uk",
     "www.bartlett.ucl.ac.uk",
     "www.cege.ucl.ac.uk",
     "www.chem.ucl.ac.uk",
     "www.cs.ucl.ac.uk",
     "www.csml.ucl.ac.uk",
     "www.ee.ucl.ac.uk",
     "www.engineering.ucl.ac.uk",
     "www.gatsby.ucl.ac.uk",
     "www.geog.ucl.ac.uk",
     "www.grad.ucl.ac.uk",
     "www.homepages.ucl.ac.uk",
     "www.icn.ucl.ac.uk",
     "www.igp.ucl.ac.uk",
     "www.laws.ucl.ac.uk",
     "www.london-in-motion.ucl.ac.uk",
     "www.mailinglists.ucl.ac.uk",
     "www.mecheng.ucl.ac.uk",
     "www.meng.ucl.ac.uk",
     "www.phon.ucl.ac.uk",
     "www.silva-sandbox.ucl.ac.uk",
     "www.star.ucl.ac.uk",
     "www.ucl.ac.uk",
     "www0.cs.ucl.ac.uk",
     "zuserver2.star.ucl.ac.uk"]

    # Define the starting pages to crawl
    start_urls = ["http://advancedteaching.cs.ucl.ac.uk",
     "http://blogs.ucl.ac.uk",
     "http://busics.cs.ucl.ac.uk",
     "http://ccs.chem.ucl.ac.uk",
     "http://crest.cs.ucl.ac.uk",
     "http://crf.casa.ucl.ac.uk",
     "http://discovery.ucl.ac.uk",
     "http://geometry.cs.ucl.ac.uk",
     "http://haig.cs.ucl.ac.uk",
     "http://iris.ucl.ac.uk",
     "http://is.cs.ucl.ac.uk",
     "http://mediafutures.cs.ucl.ac.uk",
     "http://nrg.cs.ucl.ac.uk",
     "http://onlinestore.ucl.ac.uk",
     "http://pplv.cs.ucl.ac.uk",
     "http://readinglists.ucl.ac.uk",
     "http://reality.cs.ucl.ac.uk",
     "http://sec.cs.ucl.ac.uk",
     "http://vecg.cs.ucl.ac.uk",
     "http://vis.cs.ucl.ac.uk",
     "http://web4.cs.ucl.ac.uk",
     "http://www-mice.cs.ucl.ac.uk",
     "http://www.bartlett.ucl.ac.uk",
     "http://www.cege.ucl.ac.uk",
     "http://www.chem.ucl.ac.uk",
     "http://www.cs.ucl.ac.uk",
     "http://www.csml.ucl.ac.uk",
     "http://www.ee.ucl.ac.uk",
     "http://www.engineering.ucl.ac.uk",
     "http://www.gatsby.ucl.ac.uk",
     "http://www.geog.ucl.ac.uk",
     "http://www.grad.ucl.ac.uk",
     "http://www.homepages.ucl.ac.uk",
     "http://www.icn.ucl.ac.uk",
     "http://www.igp.ucl.ac.uk",
     "http://www.laws.ucl.ac.uk",
     "http://www.london-in-motion.ucl.ac.uk",
     "http://www.mailinglists.ucl.ac.uk",
     "http://www.mecheng.ucl.ac.uk",
     "http://www.meng.ucl.ac.uk",
     "http://www.phon.ucl.ac.uk",
     "http://www.silva-sandbox.ucl.ac.uk",
     "http://www.star.ucl.ac.uk",
     "http://www.ucl.ac.uk",
     "http://www0.cs.ucl.ac.uk",
     "http://zuserver2.star.ucl.ac.uk"]

    # Define additional rules to limit crawlable_domains within allowed domains
    crawlable_domains = ["http://advancedteaching.cs.ucl.ac.uk/.*",
     "http://blogs.ucl.ac.uk/.*",
     "http://busics.cs.ucl.ac.uk/.*",
     "http://ccs.chem.ucl.ac.uk/.*",
     "http://crest.cs.ucl.ac.uk/.*",
     "http://crf.casa.ucl.ac.uk/.*",
     "http://discovery.ucl.ac.uk/.*",
     "http://geometry.cs.ucl.ac.uk/.*",
     "http://haig.cs.ucl.ac.uk/.*",
     "http://iris.ucl.ac.uk/.*",
     "http://is.cs.ucl.ac.uk/.*",
     "http://mediafutures.cs.ucl.ac.uk/.*",
     "http://nrg.cs.ucl.ac.uk/.*",
     "http://onlinestore.ucl.ac.uk/.*",
     "http://pplv.cs.ucl.ac.uk/.*",
     "http://readinglists.ucl.ac.uk/.*",
     "http://reality.cs.ucl.ac.uk/.*",
     "http://sec.cs.ucl.ac.uk/.*",
     "http://vecg.cs.ucl.ac.uk/.*",
     "http://vis.cs.ucl.ac.uk/.*",
     "http://web4.cs.ucl.ac.uk/.*",
     "http://www-mice.cs.ucl.ac.uk/.*",
     "http://www.bartlett.ucl.ac.uk/.*",
     "http://www.cege.ucl.ac.uk/.*",
     "http://www.chem.ucl.ac.uk/.*",
     "http://www.cs.ucl.ac.uk/.*",
     "http://www.csml.ucl.ac.uk/.*",
     "http://www.ee.ucl.ac.uk/.*",
     "http://www.engineering.ucl.ac.uk/.*",
     "http://www.gatsby.ucl.ac.uk/.*",
     "http://www.geog.ucl.ac.uk/.*",
     "http://www.grad.ucl.ac.uk/.*",
     "http://www.homepages.ucl.ac.uk/.*",
     "http://www.icn.ucl.ac.uk/.*",
     "http://www.igp.ucl.ac.uk/.*",
     "http://www.laws.ucl.ac.uk/.*",
     "http://www.london-in-motion.ucl.ac.uk/.*",
     "http://www.mailinglists.ucl.ac.uk/.*",
     "http://www.mecheng.ucl.ac.uk/.*",
     "http://www.meng.ucl.ac.uk/.*",
     "http://www.phon.ucl.ac.uk/.*",
     "http://www.silva-sandbox.ucl.ac.uk/.*",
     "http://www.star.ucl.ac.uk/.*",
     "http://www.ucl.ac.uk/.*",
     "http://www0.cs.ucl.ac.uk/.*",
     "http://zuserver2.star.ucl.ac.uk/.*"]

    rules = (
        Rule(LinkExtractor(allow_domains=crawlable_domains), callback='parse'),
    )

    # The method called on a document retrieval
    def parse(self, response):

        # Ignore non html responses
	if not isinstance(response, HtmlResponse):
	    return

        # Clean html responses of non-html
        clean_html = self.cleaner.clean_html(response.body)
        soup = BeautifulSoup(clean_html, "lxml")

        # Use a lock whilst tracking document numbers and urls crawled
        self.lock.acquire()
        try:
            with open('sitescrawled.txt', "a") as myfile:
                myfile.write(response.url + "\n")
            with open('sites/url' + str(self.counter), 'wb') as f:
                # Output BeautifulSoup formatted html, with additonal <url> header tag
                f.write("<url>" + response.url + "</url>\n" + soup.prettify("utf-8"))
            self.counter += 1
        finally:
            self.lock.release()

        for href in response.css("a::attr('href')"):
            # Ignore php items and hyperlink tags in the url header
            url = response.urljoin(href.extract())
            url = url.split('?')[0].split('#')[0]
            yield scrapy.Request(url)
