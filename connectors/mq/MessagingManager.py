__author__ = 'snouto'

import pika
from common import *



class DBDMessage(object):

    def __init__(self):
        self.url = ""

    def __init__(self,url):
        self.url = url

    def __str__(self):
        return self.url
    def __repr__(self):
        return self.url
    def __unicode__(self):
        return self.url


    def __len__(self):
        return len(self.url)


class MessagingManager(object):

    def __init__(self,queue=dbd_queue):
        try:
            self.credentials=pika.PlainCredentials(username=queue_username,password=queue_password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=queue_server,credentials=self.credentials))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue)
        except Exception, s:
            raise s


    def sendMessage(self,message,queue=dbd_queue):

        if not isinstance(message,DBDMessage):
            raise Exception("You should pass a DBDMessage instance object instead")
        else:
            self.channel.basic_publish(exchange='',
                                       routing_key=queue
                                       ,body=str(message))
            print("Message was sent , Contents : %s" % message)


    def consume(self,callback,queue=dbd_queue,consumer_tag="dbdconsumer"):
        self.channel.basic_consume(consumer_callback=callback,queue=queue,no_ack=True,consumer_tag=consumer_tag)
        self.channel.start_consuming()


    def stopConsuming(self,consumer_tag="dbdconsumer"):
        self.channel.stop_consuming(consumer_tag=consumer_tag)




    def closeConnection(self):
        self.connection.close() # Closes the underlying queue connection









