__author__ = 'snouto'

from common import *
from mq.MessagingManager import MessagingManager , DBDMessage
import ast
from thug import *



def start_thug_analysis(message):
    if len(message) > 0:
        payload = ast.literal_eval(message)
        # get the id
        _id = payload["_id"]
        #access the submitted urls from the crawler
        urls = payload["urls"]

        if urls:
            for url in urls:
                #begin the thug analysis
                Thug({"_id":_id,"url":url})()

            #now send notification
            notificationManager = MessagingManager(queue=notification_queue,broadcast=False)
            notify_msg = DBDMessage(payload={"name":"thug","site_id":_id})
            notify_msg.payload = {"name":"thug","site_id":_id}
            notificationManager.sendMessage(message=notify_msg,queue=notification_queue)
            notificationManager.closeConnection()
            print("Notification has been sent\n")
    else:
        print("Thug : Empty Message received , Ignoring it..........\n")




def callback(ch, method, properties, body):


    start_thug_analysis(body)


def main():

    messagingManager = None
    print("................................Starting Thug..............................\n")
    print("Starting Listening on Queue : %s \n" % crawler_queue)

    while True:
        try:
            messagingManager = MessagingManager(queue=thug_queue_name,broadcast=True)
            messagingManager.consume(callback=callback,queue=thug_queue_name,consumer_tag="thug")
        except Exception , s:
            print("Exception : %s\n" % s.message)
            print("Continuing.........\n")
            continue









if __name__ =="__main__":
    main()