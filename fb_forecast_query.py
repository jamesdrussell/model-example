import json
import pandas as pd
import requests as req

from pandas import DataFrame

class FbForecastApi:
    """Class that queries the API for you"""

    def __init__(self, dataset):
        """Return a TemperatureData initialized."""
        self.base_uri = "https://api.farmbase.io/datasets/" + dataset
        self.forecast_uri = self.base_uri + "/forecasts"

    @staticmethod
    def check_ok(http_response, msg):
    	if not http_response.ok:
    		print "Non-OK response [{0}] resp={1}".format(msg, http_response)
    		return False
    	else:
    		return True

    def forecast_q(self, lat, lon, limit):
    	# https://api.farmbase.io/datasets/gfs/forecasts?filter={"keys":["model_date","forecast_date","type","value"],"where":["$geoIntersects","geom",["$point",93.0000,42.0000]],"order":["model_date","forecast_date"]}&limit=10
    	query_clause = {"keys":["model_date,forecast_date,type,value"], "where":["$geoIntersects","geom",["$point", lon, lat]],"order":["model_date","forecast_date"]}
    	s = json.dumps(query_clause)
    	payload = {'filter': s,
    			   'limit': limit}
    	r = req.get(self.forecast_uri, params=payload)
    	return r

    def forecast_as_df(self, lat, lon, datatype, limit):
    	forecast_results = self.forecast_q(lat, lon, limit)
    	if not FbForecastApi.check_ok(forecast_results, "forecast_q"):
    		return None

    	forecast_data = forecast_results.json()['results']
    	if bool(forecast_data):
    		forecast_results_df = DataFrame(forecast_data)
    		forecast_results_df.rename(columns = {'value' : datatype}, inplace=True)
    		forecast_results_df['forecast_date'] = forecast_results_df['forecast_date'].astype('datetime64[ns]')
    		forecast_results_df['model_date'] = forecast_results_df['model_date'].astype('datetime64[ns]')
    		return forecast_results_df
    	else:
    		return None