__author__ = 'snouto'

from common import *
from scrapy.crawler import CrawlerProcess
from crawler.DBDCrawler import DBDCrawler
from twisted.internet import reactor
from mq.MessagingManager import MessagingManager , DBDMessage
import scrapydo


scrapydo.setup()


messageManager = None

def callback(ch, method, properties, body):
    print("Received A URL with Payload : %s\n" % body)
    print("Start Crawling on that url : %s\n"%body)
    response = scrapydo.fetch(url=body,spider_cls=DBDCrawler)
    crawler = DBDCrawler()
    crawler.crawl(body)
    if not response == None and len(response.body) > 0:
        crawler.parse(response)





if __name__ =="__main__":
    print("Starting the Message Manager to listen on Queue Named : %s\n" % dbd_queue)
    messageManager = MessagingManager(queue=dbd_queue)
    print("Started On Queue : %s" % dbd_queue)
    print ("Starting Consuming Message on the same Queue\n")
    messageManager.consume(callback=callback,queue=dbd_queue,consumer_tag="dbdCrawler")

