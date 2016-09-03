__author__ = 'snouto'

from db.AnalysisGrabber import AnalysisGrabber
from time import gmtime, strftime

class AnalysisCollector(object):



    def __init__(self,site):
        self.grabber = AnalysisGrabber(site)
        self.site = site



    def getAll(self):
        #first we access the site Collection
        oneSite = self.grabber.get_One_site(site=self.site)
        print("%s",oneSite)
        finalResult = {}
        finalResult.__setitem__("domain",oneSite['domain'])
        finalResult.__setitem__("url",oneSite['domain'])
        finalResult.__setitem__("urls_count",len(oneSite['urls']))
        finalResult.__setitem__("creationDate",str(strftime("%a, %d %b %Y %H:%M:%S", gmtime())))
        #get phoneyC results
        phoneyc_data = self.grabber.get_phoneyc(oneSite["_id"])
        phoneyc = {}
        if not phoneyc_data == None:
            phoneyc.__setitem__("url",phoneyc_data['url'])
            phoneyc.__setitem__("filename",phoneyc_data['filename'])
            phoneyc.__setitem__("alerts",phoneyc_data['alerts'])
            finalResult.__setitem__("phoneyc",phoneyc)

        # now get thug related analysis
        thug = {}
        #get urls collection
        urls = self.grabber.get_urls_collection()
        #get analysis
        analyses = self.grabber.get_analysis()
        url = urls.find_one({"_id":analyses['url_id']})
        analyses['url'] = url
        thug.__setitem__("analyses",analyses)
        #get behaviors
        behaviors_data = self.grabber.get_behaviors(analysis_id=analyses['_id'])
        behaviors = []
        for behavior in behaviors_data:
            one_behavior = {
                "cve":behavior['cve'],
                "time":str(strftime("%a, %d %b %Y %H:%M:%S", gmtime())),
                "method":behavior['method'],
                "description":behavior['description']
            }
            behaviors.append(one_behavior)
        thug.__setitem__("behaviors",behaviors)
        #get codes
        codes_data = self.grabber.get_codes(analysis_id=analyses['_id'])
        codes = []
        for code in codes_data:
            one_code = { "relationship" : code['relationship'],
                         "snippet":code['snippet'],
                         "language":code['language'],
                         "method":code['method']
            }
            codes.append(one_code)

        thug.__setitem__("codes",codes)

        #get connections
        connections_data = self.grabber.get_connections(analysis_id=analyses['_id'])
        connections =[]

        for connection in connections_data:
            one_connection = {
                "source" : urls.find_one({"_id":connection['source_id']}),
                "destination" : urls.find_one({"_id":connection['destination_id']}),
                "method" : connection['method']
            }
            connections.append(one_connection)

        thug.__setitem__("connections",connections)

        #get exploits
        exploits_data = self.grabber.get_exploits(analysis_id=analyses['_id'])
        exploits =[]
        for exploit in exploits_data:
            one_exploit = {

                "cve" : exploit['cve'],
                "module":exploit['module'],
                "url" : urls.find_one({"_id":exploit['url_id']}),
                "data" : exploit['data'],
                "description" : exploit['description']
            }
            exploits.append(one_exploit)

        thug.__setitem__("exploits",exploits)

        #get locations
        locations_data = self.grabber.get_locations(analysis_id=analyses['_id'])
        locations = []

        for location in locations_data:
            one_location = {
                "size" : location['size'],
                "md5" : location['md5'],
                "sha256" : location['sha256'],
                "url" : urls.find_one({"_id":location['url_id']})
            }
            locations.append(one_location)

        thug.__setitem__("locations",locations)

        finalResult.__setitem__("thug",thug)

        #close the database connection to save memory and IO
        self.grabber.closeConnection()




        return finalResult


