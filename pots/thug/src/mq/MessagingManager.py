__author__ = 'snouto'

import pika
from common import *



class DBDMessage(object):

    def __init__(self):
        self.payload = ""

    def __init__(self,payload):
        self.payload = payload

    def __str__(self):
        return str(self.payload)
    def __repr__(self):
        return str(self.payload)
    def __unicode__(self):
        return str(self.payload)


    def __len__(self):
        return len(str(self.payload))


class MessagingManager(object):

    def __init__(self,queue=dbd_queue,broadcast=False):
        try:
            self.broadcast = broadcast
            self.credentials=pika.PlainCredentials(username=queue_username,password=queue_password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=queue_server,credentials=self.credentials))
            self.channel = self.connection.channel()

            # if the broadcast is set to True , that means we are going to use Exchange fanout to broadcast the messages to all listening parties
            if self.broadcast:
                self.channel.exchange_declare(exchange=crawler_exchange_name,exchange_type=crawler_exchange_type)

            self.channel.queue_declare(queue=queue)

        except Exception, s:
            raise s


    def sendMessage(self,message,queue=dbd_queue):

        if not isinstance(message,DBDMessage):
            raise Exception("You should pass a DBDMessage instance object instead")
        else:
            if self.broadcast:
                self.channel.basic_publish(exchange=crawler_exchange_name,
                                       routing_key=queue
                                       ,body=str(message))
            else:
                self.channel.basic_publish(exchange='',
                                       routing_key=queue
                                       ,body=str(message))
            print("Message was sent , Contents : %s" % message)


    def consume(self,callback,queue=dbd_queue,consumer_tag="dbdconsumer"):

        # if the broadcast is set to True , that means we should bind the exchange to the queue
        if self.broadcast:
            self.channel.queue_bind(queue=queue,exchange=crawler_exchange_name,routing_key=consumer_tag)

        self.channel.basic_consume(consumer_callback=callback,queue=queue,no_ack=True,consumer_tag=consumer_tag)
        self.channel.start_consuming()


    def stopConsuming(self,consumer_tag="dbdconsumer"):
        self.channel.stop_consuming(consumer_tag=consumer_tag)




    def closeConnection(self):
        self.connection.close() # Closes the underlying queue connection









