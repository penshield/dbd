__author__ = 'snouto'


from pymongo import MongoClient
from common import *

class AnalysisGrabber(object):

    def __init__(self,site):
        self.site = site
        self.client = MongoClient(host=DATABASE_HOST,port=DATABASE_PORT)
        self.db = self.client[DATABASE_NAME]
        self.analyses = None





    def get_sites_collection(self):
        self.sites = self.db['sites']
        return self.sites


    def get_One_site(self,site):
        self.get_sites_collection()
        return self.sites.find_one({"_id":site})



    def get_analysis(self):
        self.get_analysis_collection()
        return self.analyses.find_one({"site_id":self.site})


    def get_analysis_collection(self):
         self.analyses = self.db['analyses']
         return self.analyses


    def get_behaviors(self,analysis_id):
        self.get_behavior_collection()
        return self.behaviors.find({"analysis_id":analysis_id})

    def get_behavior_collection(self):
        self.behaviors = self.db['behaviors']
        return self.behaviors


    def get_codes(self,analysis_id):
        self.get_codes_collection()
        return self.codes.find({"analysis_id":analysis_id})

    def get_codes_collection(self):
        self.codes = self.db['codes']
        return self.codes



    def get_connections(self,analysis_id):
        self.get_connections_collection()
        return self.connections.find({"analysis_id":analysis_id})

    def get_connections_collection(self):
        self.connections = self.db['connections']
        return self.connections

    def get_exploits(self,analysis_id):
        self.get_exploits_collection()
        return self.exploits.find({"analysis_id":analysis_id})


    def get_exploits_collection(self):
        self.exploits = self.db['exploits']
        return self.exploits

    def get_locations(self,analysis_id):
        self.get_locations_collection()
        return self.locations.find({"analysis_id":analysis_id})

    def get_locations_collection(self):
        self.locations = self.db['locations']
        return self.locations

    def get_phoneyc(self,site_id):
        self.get_phoneyc_collection()
        return self.phoneyc.find_one({"site_id":site_id})


    def get_phoneyc_collection(self):
        self.phoneyc = self.db['phoneyc_analysis']
        return self.phoneyc


    def get_urls_collection(self):
        self.urls = self.db["urls"]
        return self.urls



    def closeConnection(self):

        if not self.client == None:
            self.client.close()









