import json
import pandas as pd
import requests as req

from pandas import DataFrame

class FbStationsApi:
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
    	# https://api.farmbase.io/datasets/ghcn/stations?limit=10&where={"name":{"geom":{"$geoWithin":{"$center":[[-122.32,38.50],0.1]}}}}
    	query_clause = {"*" : {"geom" : {"$geoWithin":{"$center":[[lon, lat], radius]}}}, "station_id":{"$like":"USC0%"}}
    	s = json.dumps(query_clause)
    	payload = {'keys': 'station_id,name,min_date', 
    			   'where': s,
    			   'limit': limit}
    	r = req.get(self.stations_uri, params=payload)
    	return r

    def obs_for_station_q(self, station_id, datatype, limit):
    	# http://api.farmbase.io/ghcn/observations?keys=date,value&limit=10&where={"station":"CA002303986","datatype":"TMIN"}
    	query_clause = {"station": station_id, "datatype": datatype}
    	s = json.dumps(query_clause)
    	payload = {'keys': 'date,value', 
    			   'where': s,
    			   'limit': limit}
    	r = req.get(self.obs_uri, params=payload)
    	return r

    def obs_for_station_as_df(self, station_id, datatype, limit):
    	obs_results = self.obs_for_station_q(station_id, datatype, limit)
    	if not FbStationsApi.check_ok(obs_results, "obs_for_station_q"):
    		return None

    	obs_data = obs_results.json()['results']
    	if bool(obs_data):
    		obs_results_df = DataFrame(obs_data)
    		obs_results_df.rename(columns = {'value' : datatype}, inplace=True)
    		obs_results_df['date'] = obs_results_df['date'].astype('datetime64[ns]')
    		return obs_results_df
    	else:
    		return None

    def get_station_with_data(self, lat, lon, datatype):
    	results = self.stations_by_radius_q(lat, lon, 0.2, 50)
    	if not FbStationsApi.check_ok(results, "stations_by_radius_q"):
    		return None

    	stations = results.json()['results']
    	if not bool(stations):
    		print "No station found for [{0},{1}]".format(lat, lon)
    		return None
    	
    	stations_df = DataFrame(stations)

    	for station_id in stations_df['station_id']:
    		print "Querying station: {0}\n".format(station_id)
    		obs_results = self.obs_for_station_q(station_id, datatype, 2)

    		if not FbStationsApi.check_ok(obs_results, "obs_for_station_q"):
    			return None

    		obs_data = obs_results.json()['results']
    		if bool(obs_data):
    			print "Found a station {0} with data {1}\n".format(station_id, obs_data)
    			return station_id


#dsq = fb_query.FbApi("ghcn")
#t = dsq.stations_by_radius_q(38.5,-122.32,0.1,10)