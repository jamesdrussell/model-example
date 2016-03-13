import json
import requests as req

from pandas import DataFrame

class FbApi:
    """Class that queries the API for you"""

    def __init__(self, dataset):
        """Return a TemperatureData initialized."""
        self.base_uri = "https://api.farmbase.io/datasets/" + dataset
        self.stations_uri = self.base_uri + "/stations"
        self.obs_uri = self.base_uri + "/observations"

    @staticmethod
    def check_ok(http_response, msg):
    	if not http_response.ok:
    		print "Non-OK response [{0}] resp={1}".format(msg, http_response)
    		return False
    	else:
    		return True

    def stations_by_radius_q(self, lat, lon, radius, limit):
    	# http://api.farmbase.io/ghcn/stations?keys=station_id,name,min_date&where={"geom":{"$geoWithin":{"$center":[[-122.32,38.50],0.1]}}}&limit=10
    	query_clause = {"*" : {"geom" : {"$geoWithin":{"$center":[[lon, lat], radius]}}}}
    	s = json.dumps(query_clause)
    	payload = {'keys': 'station_id,name,min_date', 
    			   'where': s,
    			   'limit': limit}
    	r = req.get(self.stations_uri, params=payload)
    	return r