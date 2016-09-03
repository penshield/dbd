__author__ = 'snouto'


import poplib
from common import *
from email.parser import Parser

class PopManager(object):

    def __init__(self):
        self.manager = poplib.POP3_SSL(host=POP_HOST)
        self.manager.user(POP_USERNAME)
        self.manager.pass_(POP_PASSWORD)


    def get_message_with_subject(self,subjects):

        self.numOfMessages = [i for i in range(1,len(self.manager.list()[1])+1)]
        self.messages = [self.manager.retr(i) for i in range(1,len(self.manager.list()[1])+1)]
        self.messages = ["\n".join(msg[1]) for msg in self.messages ]
        self.email_parser = Parser()
        self.messages = [self.email_parser.parsestr(msg) for msg in self.messages]
        email_messages = []

        for message in self.messages:
            msg_subject = message['subject']
            if msg_subject.lower() in subjects:
                for part in message.walk():
                    if part.get_content_type() == 'text/plain':
                        message_body = part.get_payload(decode=True)

                        if message_body != None:
                            email_message = {'subject':msg_subject,
                                             'body':message_body}
                            email_messages.append(email_message)

        #self.delete_messages(self.numOfMessages)


        return email_messages



    def delete_messages(self,numofMessages):
        if len(numofMessages) > 0:

            for i in numofMessages:
                self.manager.dele(i)





    def close_popper(self):
        self.manager.quit()






