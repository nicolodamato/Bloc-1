import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class CitiesSpider(scrapy.Spider):

    name = "cities" # define the name

    start_urls = [
        'https://one-week-in.com/35-cities-to-visit-in-france/', # define the start url
    ]

    def parse(self, response):
        n = 35
        for i in range(n): # create à loop to get our cities
            i = i + 1
            # create a dictionnary containing cities names
            yield {
                'City': response.xpath('//*[@id="main"]/article/div/div[2]/ol/li[{}]/a/text()'.format(i)).get(),
            }
# define the filename of our json
filename = "response_cities.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('src2/'):
        os.remove('src2/' + filename)

# define the user agent
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src2/' + filename : {"format": "json"},
    }
})

process.crawl(CitiesSpider)
process.start()