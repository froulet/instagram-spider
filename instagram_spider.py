# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
import os


class InstagramSpider(scrapy.Spider):
    name = "Instagram"  # Name of the Spider, required value

    def __init__(self, account=''):
        self.start_urls = ["https://www.instagram.com/"+account]
        self.account = account

    # Entry point for the spider
    def parse(self, response):
        if not os.path.exists(self.account):
            os.makedirs(self.account)

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
            self.save_image(url, id, self.account)
        #If there is a next page, we crawl it
        if has_next:
            url="https://www.instagram.com/"+self.account+"/?max_id="+media[-1]['id']
            return scrapy.Request(url, callback=self.parse_page)

        

    @staticmethod
    def pwrite(text):
        with open('comments.txt', 'a') as f:        
                f.write(str(text))

    
    #We grab the photo with urllib
    @staticmethod            
    def save_image(url, id, dir):
        print(url)
        fullfilename = os.path.join(dir, id+'.jpg')
        urllib.urlretrieve(url, fullfilename)
