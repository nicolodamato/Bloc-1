import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class CitiesSpider(scrapy.Spider):

    name = "cities"

    start_urls = [
        'https://one-week-in.com/35-cities-to-visit-in-france/',
    ]

    def parse(self, response):
        n = 35
        for i in range(n):
            i = i + 1
            yield {
                'City': response.xpath('//*[@id="main"]/article/div/div[2]/ol/li[{}]/a/text()'.format(i)).get(),
            }
            
filename = "response_cities.json"

if filename in os.listdir('src2/'):
        os.remove('src2/' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src2/' + filename : {"format": "json"},
    }
})

process.crawl(CitiesSpider)
process.start()