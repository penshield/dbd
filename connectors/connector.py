__author__ = 'snouto'

from flask import Flask , request

from mq.MessagingManager import MessagingManager , DBDMessage


app = Flask(__name__)

app.debug = True



@app.route('/dbd/add',methods=['POST','GET'])
def launcher():

    url = request.args['url']

    if len(url) <= 0 :
        return dict(message="Submitted url is empty , please provided a valid url",code=500).__str__()
    else:
        try:

            messagingManager = MessagingManager(broadcast=False)


            dbd_message = DBDMessage(url)
            #save it into the database
            messagingManager.sendMessage(dbd_message)
            #close the connection to the channel
            messagingManager.closeConnection()
            return dict(message="Successfully Received the URL and has been submitted to the Queue",code=200).__str__()


        except Exception,s:
            print ("There was an exception : %s" % s.message)
            return dict(message="unable to connect to the messaging queue",code=500).__str__()










if __name__ == '__main__':

    app.run()



