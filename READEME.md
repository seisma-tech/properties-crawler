# Get Started with Python Scrapy
## Web Crawler for crawling and scraping properties data from https://www.domain.com.au


- In the project directory, you can run:
```
pip3 install scrapy
```

- This is testing version, using fixed url as a target:
- ```https://www.domain.com.au/sale/melbourne-region-vic/town-house/?excludeunderoffer=1&establishedtype=new```

+ start crawling command line without output file:
+ ```scrapy crawl domain```

- start with output file with json file
- ```scrapy crawl domain -o filename.json```