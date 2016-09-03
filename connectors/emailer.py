__author__ = 'snouto'

from common import *
from notifications.EmailManager import EmailManager
from mq.MessagingManager import MessagingManager
from db.AnalysisCollector import  AnalysisCollector
from jinja2 import Environment, FileSystemLoader
import jinja2
import json

import ast



def callback(ch, method, properties, body):

    if not body == None and len(body) > 0:
        payload = ast.literal_eval(body)
        site_id = payload['site_id']
        collector = AnalysisCollector(site=site_id)
        result = collector.getAll()

        env = Environment(loader=FileSystemLoader(notification_templates_url),undefined=jinja2.StrictUndefined)
        template = env.get_template("template.html")
        message = template.render(result=result)
        print(message)
        #print(json.dumps(result.__str__(),separators=[',',':'],indent=4))
        print("\n")
        emailManager = EmailManager(From="apps@is.com.sa",To="mfawzy@is.com.sa",username="apps@is.com.sa",password="M@safsafsaF")
        emailManager.setEmail("Automated Sandboxing Analysis Results",message)
        emailManager.sendNotification()
        print("Message has been sent successfully.\n")






def main():

    messagingManager = None

    print ("Starting Notification Service\n")
    print("Listening on Queue : %s\n" % notification_queue)
    while True:
        try:
            messagingManager = MessagingManager(queue=notification_queue,broadcast=False)
            messagingManager.consume(callback=callback,queue=notification_queue,consumer_tag="Notifier")
        except Exception, s:
            print("Mailer : Exception , %s\n" % s.message)
            if not messagingManager == None:
                messagingManager.closeConnection()
            continue


if __name__ =="__main__":
    main()