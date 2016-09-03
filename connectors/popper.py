__author__ = 'snouto'


from pop.pop import PopManager
from mq.MessagingManager import MessagingManager , DBDMessage
import re










def main():
    popper = None

    closed = False

    while True:
        try:
            popper = PopManager()
            subjects = ['analysis','analyze','analyse','analyses']

            messages = popper.get_message_with_subject(subjects)

            if len(messages) > 0:

                for message in messages:
                    for subject , body in message.items():
                        # get all urls from the body
                        urls = re.findall(r"(https?://\S+)",body)
                        if len(urls) > 0:
                            messagingManager = MessagingManager(broadcast=False)

                            for url in urls:

                                dbd_message = DBDMessage(url)
                                #save it into the database
                                messagingManager.sendMessage(dbd_message)
                                print("\n")
                            messagingManager.closeConnection()



            popper.close_popper()







        except Exception ,s :
            print (s.message)
            if popper != None:
                print ("Closing the connection")
                popper.close_popper()












if __name__ =="__main__":
    main()