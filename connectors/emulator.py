#!/usr/bin/env python
"""
Synopsis:
    PHoneyC: Pure python honeyclient implementation.

Usage:
    python phoneyc.py [ options ] url

Options:
    -h              , --help                        Display this help information.
    -l <filename>   , --logfile=<filename>          Output file name for logs.
    -v              , --verbose                     Explain what is being done (DEBUG mode).
    -d <debuglevel> , --debug=<debuglevel>          Debug Level, 1-10.
    -r              , --retrieval-all               Retrieval all inline linking data.
    -c              , --cache-response              Cache the responses from the remote sites.
    -u <personality>, --user-agent=<personality>    Select a user agent (see below for values, default: 2)
    -n              , --replace-nonascii            Replace all non-ASCII characters with spaces(0x20) in all HTML or JS contents
    -m              , --universal-activex           Enable Universal ActiveX object 
"""

import sys, os, shutil 
import pycurl
import hashlib
import site
import getopt
from binascii import hexlify

site.addsitedir('lib/python')

from emulator import config
from emulator import magic
from common import *
from mq.MessagingManager import MessagingManager , DBDMessage
import ast



USAGE_TEXT = __doc__

def usage():
    print USAGE_TEXT
    print "User Agents:"
    for ua in config.UserAgents:
        print "    [%2d] %s" % (ua[0], ua[1], )
    print ""
    sys.exit(1)

def check_logdirs():
    for logdir in LOGDIRS:
        if not os.access(logdir, os.F_OK):
            try:
                os.makedirs(logdir)
            except OSError:
                pass

def download(url):
    import urlparse

    f = hashlib.md5()
    f.update(url)
    exec_name = url.split('/')[-1]
    print("File name is : %s" % exec_name)
    filename = "%s/%s" % (BINARIES_DIR, exec_name, )

    fd = open(filename, 'wb')
    ua = config.userAgent
    
    c = pycurl.Curl()
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.URL, str(url))
    c.setopt(pycurl.WRITEDATA, fd)
    c.setopt(pycurl.USERAGENT, ua)

    try:
        c.perform()
        code = c.getinfo(pycurl.HTTP_CODE) 
        if code == 404:
            config.VERBOSE(config.VERBOSE_DEBUG,
                           "[DEBUG] 404 File Not Found: "+url)
            fd.close()
            os.remove(filename)
            return
    except:
        import traceback
        traceback.print_exc(file = sys.stderr)
        sys.stderr.flush()

    c.close()
    fd.close()

    statinfo = os.stat(filename)
    if not statinfo.st_size:
        os.remove(filename)
        return

    fd = open(filename, 'r')
    h = hashlib.md5()
    h.update(fd.read())
    newfilename = "%s/%s" % (BINARIES_DIR, exec_name, )
    shutil.move(filename, newfilename)
    fd.close()

def report(alerts,id,filename,analyzed_url):
    from bson.objectid import ObjectId
    from db.DatabaseManager import DatabaseManager
    #create the database manager in here
    databaseManager = DatabaseManager()
    #creating a record
    record = {"_id":ObjectId(),"id":id,"url":analyzed_url,"filename":filename,"alerts":[]}

    if alerts: # check to see if alerts are not empty
        for alert in alerts:

            if alert.atype == "ALERT_SHELLCODE":
                #run the shellcode
                shellCode_result = alert.run_shellcode()

                alert_record = {"type":str(alert.atype),
                                "aid":str(alert.aid),
                                "message":str(alert.msg),
                                "misc":str(alert.misc),
                                "length":len(str(alert.shellcode)),
                                "shellcode" : str(hexlify(alert.shellcode)),
                                "shellcodeResult" : str(shellCode_result),
                                "executables":[]
                                }
                # now check the shellcode result
                for item in shellCode_result:
                    if item['name'] == 'URLDownloadToFile':
                        url = item['arguments'][1][2][2]
                        execs = alert_record['executables']
                        execs.append(url)
                        #download the file
                        print("Downloading file From : %s" % url)
                        download(url)
                # add the alert record into the parent record
                record['alerts'].append(alert_record)

            if alert.atype == "ALERT_HEAPSPRAY" and alert.entropy < 1:

                 record['alerts'].append({"type":str(alert.atype),
                                "aid":str(alert.aid),
                                "message":str(alert.msg),
                                "misc":str(alert.misc),
                                "length":len(str(alert.length)),
                                "hit":str(alert.hit),
                                "memusage":str(alert.memusage),
                                "entropy":str(alert.entropy)
                                })
        #now save the total record into the database
        databaseManager.insert(record)
        print("The current Analysis has been saved into the database")
    else:
        print ("The analyzed Url seems not malicious in nature")

    #closes the connection to the database
    databaseManager.close()



def callback(ch, method, properties, body):

    if not body == None and len(body) > 0:
        #get the payload
        payload = ast.literal_eval(body)
        url = payload['url']
        id = payload['id']
        filename = payload['filename']
        #we should save the data into the database
        config.initial_URL = url
        from DOM.DOM import DOM
        phoneycdom = DOM(config.initial_URL)
        alerts = phoneycdom.analyze()
        if alerts:
            report(alerts,id,filename,url)
        else:
            print("No Alerts , The website seems ok")


if __name__ == "__main__":
    print("Started Listening on Queue : %s" % crawler_queue)
    messagingManager = MessagingManager(queue=crawler_queue)
    messagingManager.consume(callback=callback,queue=crawler_queue,consumer_tag="DBEmulator")





