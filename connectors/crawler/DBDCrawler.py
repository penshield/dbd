__author__ = 'snouto'

import scrapy
from urlparse import urlparse
from common import *
from scrapy.contrib.linkextractors.lxmlhtml import LxmlParserLinkExtractor
import hashlib
import time
from mq.MessagingManager import MessagingManager , DBDMessage


class DBDCrawler(scrapy.Spider):

    name =""
    start_urls =[]
    allowed_domains =[]
    response = None



    def __init__(self):
        self.name="DBDCrawler"

    def __init__(self,name='DBDCrawler'):
        self.name = name


    def crawl(self,url):
        #begin parsing the url first
        self.__parse_url__(url)
        self.start_urls = [url]



    def parse(self, response):
        millis = int(round(time.time() * 1000))
        digest = hashlib.md5(str(millis))
        filename = HTML_DIR + "/" + self.allowed_domains[0]+"-"+str(digest.hexdigest())+".html"
        with open(filename,"wb") as file:
            file.write(response.body)
        # now we should send a message to a specific queue for
        message = DBDMessage(response.body)
        message.url = dict(url=self.start_urls[0],id=digest.hexdigest(),filename=filename).__str__()
        messageManager = MessagingManager(queue=crawler_queue)
        messageManager.sendMessage(message,queue=crawler_queue)
        messageManager.closeConnection()



    def __parse_url__(self,url):
        parsed_url = urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_url)
        self.allowed_domains = [domain]

