__author__ = 'snouto'

from common import *
from crawler.DBDCrawler import DBDCrawler
from mq.MessagingManager import MessagingManager
import scrapydo

scrapydo.setup()


messageManager = None

def callback(ch, method, properties, body):

    if not body == None and len(body) > 0:
        print("Received A URL with Payload : %s\n" % body)
        print("Start Crawling on that url : %s\n"% body)
        response = scrapydo.fetch(url=body,spider_cls=DBDCrawler)
        crawler = DBDCrawler()
        crawler.crawl(body)
        if not response == None and len(response.body) > 0:
            crawler.parse(response)





if __name__ =="__main__":

    messageManager = None

    while True:
        try:
            print("Starting the Message Manager to listen on Queue Named : %s\n" % dbd_queue)
            messageManager = MessagingManager(queue=dbd_queue,broadcast=False)
            print("Started On Queue : %s" % dbd_queue)
            print ("Starting Consuming Message on the same Queue\n")
            messageManager.consume(callback=callback,queue=dbd_queue,consumer_tag="dbCrawler")
        except Exception , s:
            print("There was an exception : %s\n" % s.message)
            print("................ignoring the exception , Continuing..................\n")
            if not messageManager == None:
                messageManager.closeConnection()
                messageManager = None
            continue



