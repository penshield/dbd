__author__ = 'snouto'


dbd_queue = "dbd"
queue_server = "192.168.1.6"
queue_username="admin"
queue_password="admin"
queue_virtualHost = "/"
crawler_queue = "crawler"
DOWNLOADS_DIR = "log/downloads"
HTML_DIR="log/html"
BINARIES_DIR  = "%s/binaries" % (DOWNLOADS_DIR, )
PDF_DIR       = "%s/pdf"      % (DOWNLOADS_DIR, )
APPLET_DIR    = "%s/applet"   % (DOWNLOADS_DIR, )
MISC_DIR      = "%s/misc"     % (DOWNLOADS_DIR, )
LOGDIRS       = (BINARIES_DIR,
                 PDF_DIR,
                 APPLET_DIR,
                 MISC_DIR)
DOWNLOADS_STR = ["data", ]



# the database settings goes here
DATABASE_HOST="192.168.1.6"
DATABASE_PORT=27017
DATABASE_NAME="honeypot"
DATABASE_COLLECTION="sites"
