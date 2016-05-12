# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
import os


class InstagramSpider(scrapy.Spider):
    name = "Instagram"  # Name of the Spider, required value
    start_urls = ["https://www.instagram.com/youraccount/"]  # The starting url, Scrapy will request this URL in parse

    # Entry point for the spider
    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_page)
        return request


    # Method for parsing a page
    def parse_page(self, response):
        js = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()
        js = js[0].replace("window._sharedData = ", "")
        jscleaned = js[:-1]
        #print(jscleaned)
        locations = json.loads(jscleaned)
        #On vérifie la présence éventuelle d'une prochaine page
        has_next = locations['entry_data']['ProfilePage'][0]['user']['media']['page_info']['has_next_page']
        print(has_next)

        media = locations['entry_data']['ProfilePage'][0]['user']['media']['nodes']
        #print (media)
        for photo in media:
            url = photo['display_src']
            id =  photo['id']
            self.save_image(url, id)
        #If there is a next page, we crawl it
        if has_next:
            url="https://www.instagram.com/youraccount/?max_id="+media[-1]['id']
            return scrapy.Request(url, callback=self.parse_page)

        

    @staticmethod
    def pwrite(text):
        with open('comments.txt', 'a') as f:        
                f.write(str(text))

    
    #We grab the photo with urllib
    @staticmethod            
    def save_image(url, id):
        print(url)
        fullfilename = os.path.join("imgs/", id+'.jpg')
        urllib.urlretrieve(url, fullfilename)
