import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import json

class QuotesSpider(scrapy.Spider):

    name = "hotels" # define the name
    init_url = dict() # create a dictionnary for the urls
    start_urls = ["https://www.booking.com/"]

    # open our first json containing the cities name
    with open("src2/response_cities.json", 'r') as r:
        cities = json.load(r)
    # create a list containing cities
    list_of_cities = [[city for key, city in ele.items()] for ele in cities]

    def parse(self, response):
        for city in self.list_of_cities: # create a loop in order to get each page of each city
            yield scrapy.FormRequest.from_response(response,
                                                   formdata = {'ss': city},
                                                   callback = self.after_search, # create a callback 
                                                   meta = {'city': city})

    def after_search(self, response):

    # Callback function that will be called when starting your spider
    # It will get text, author and tags of all the <div> with class="quote" 
    # after looking the website booking.com, use css will be more appropriate
    # define hotels variable containing the first css path 
        hotels = response.css('div.a826ba81c4.fe821aea6c.fa2f36ad22.afd256fc79.d08f526e0d.ed11e24d01.ef9845d4b3.da89aeb942')
        city = response.request.meta["city"] # city is the final value of the request.meta attribute
        for hotel in hotels: 

                hotel_name = hotel.css('.a23c043802::text').get() # get the hotel name 
                hotel_score = hotel.css('div.b5cd09854e.d10a6220b4::text').get() # get the hotel score
                hotel_description = hotel.css('div.d8eab2cf7f::text').get() # get the hotel description
                hotel_url = hotel.css('a::attr(href)').get() # get the hotel url

                # create a dictionnary containing our values
                cities_dict= {
                    'city': city,
                    'hotel_name': hotel_name,
                    'score' : hotel_score,
                    'description' : hotel_description,
                    'url' : hotel_url
                }
                
                # use follow method to click the url and get gps coordinates
                yield response.follow(url=hotel_url, callback=self.gps, meta={"cities_dict": cities_dict})
    
    # create a gps fonction to get coordinates following the url
    def gps(self, response):

        data = response.request.meta["cities_dict"] 
        gps = response.css('#hotel_address::attr(data-atlas-latlng)').get() # get hotels coordinates

        data['gps'] = gps 
        
        yield data



# Name of the file where the results will be saved
filename = "hotels.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir():
        os.remove(filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        filename : {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(QuotesSpider)
process.start()