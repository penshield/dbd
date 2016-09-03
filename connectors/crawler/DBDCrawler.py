import bson

__author__ = 'snouto'

from urlparse import urlparse
from common import *
import hashlib
import time
from mq.MessagingManager import MessagingManager , DBDMessage
from scrapy.utils.spider import DefaultSpider
from db.DatabaseManager import DatabaseManager


class DBDCrawler(DefaultSpider):

    name =""
    start_urls =[]
    allowed_domains =[]
    response = None



    def __init__(self):
        self.name="DBDCrawler"

    def __init__(self,name='DBDCrawler'):
        self.name = name


    def crawl(self,message):
        #set the payload
        #TODO : if you want to crawl all pages in the passed website , you can do it in here
        #begin parsing the url first
        self.__parse_url__(message)
        self.start_urls = [message]



    def parse(self, response):
        millis = int(round(time.time() * 1000))
        digest = hashlib.md5(str(millis))
        filename = HTML_DIR + "/" + self.allowed_domains[0]+"-"+str(digest.hexdigest())+".html"
        with open(filename,"wb") as file:
            file.write(response.body)
        # now we should send a message to a specific queue for
        _id = bson.ObjectId()
        record = {
            "_id":str(_id),
            "domain":str(self.allowed_domains[0]),
            "urls" : self.start_urls,
            "hash_id":str(digest.hexdigest()),
            "filename":filename
        }
        #save that record into the database
        databaseManager = DatabaseManager()
        databaseManager.insert(record)
        databaseManager.close()
        message = DBDMessage(payload=record.__str__())
        message.payload = record.__str__()
        messageManager = MessagingManager(queue=crawler_queue,broadcast=True)
        messageManager.sendMessage(message,queue=crawler_queue)
        messageManager.closeConnection()



    def __parse_url__(self,url):
        parsed_url = urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_url)
        self.allowed_domains = [domain]

