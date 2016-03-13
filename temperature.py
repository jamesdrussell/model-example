import fb_query as fbq
import math as m
import pandas as pd

from pandas import DataFrame

class GhcnTemperatureData:
    """Class that wraps temperature (tmax & tmin) time-series"""

    def __init__(self):
        """Return a TemperatureData initialized."""
        self.dsq = fbq.FbApi("ghcn")

    def get_data_as_df(self, lat, lon, count):
    	station_id = self.dsq.get_station_with_data(lat, lon, "TMIN")
    	if station_id is None:
    		print "No station with data for [{0},{1}]".format(lon, lat)
    		return None

    	tmin_df = self.dsq.obs_for_station_as_df(station_id, "TMIN", count)
    	tmax_df = self.dsq.obs_for_station_as_df(station_id, "TMAX", count)

    	# put the TMAX col into tmin_df 
    	# tmin_df.columns => Index([u'date', u'TMIN', u'TMAX'], dtype='object')
    	tmin_df["TMAX"] = tmax_df["TMAX"]

    	# indexed_df.columns => Index([u'TMIN', u'TMAX'], dtype='object')
    	# indexed_df.index => 
    	# DatetimeIndex(['2007-01-01 08:00:00', '2007-01-02 08:00:00',
        #                '2007-01-03 08:00:00', '2007-01-04 08:00:00',
        #  ....
        #  dtype='datetime64[ns]', name=u'date', length=200, freq=None
    	t_index_df = tmin_df.set_index(keys=['date'])
    	return t_index_df

class TemperatureData:
    @staticmethod
    def pd_timestamp_to_yymm(timestamp):
    	return (timestamp.year * 100) + timestamp.month

    @staticmethod
    def monthly_temperature_aggregates(temperature_df):
    	start_yy_mm = TemperatureData.pd_timestamp_to_yymm(temperature_df.index[0])
    	result = DataFrame(	columns = ['ndays', 'SUM_TMAX', 'SUM_TMIN', 'month'])

    	for e in temperature_df.iterrows():
    		yy_mm = TemperatureData.pd_timestamp_to_yymm(e[0])
    		if not yy_mm in result.index:
    			result.loc[yy_mm] = { 'ndays' : 0, 'SUM_TMAX' : 0.0, 'SUM_TMIN': 0.0, 'month' : e[0].month}
    		tmin = e[1].TMIN
    		tmax = e[1].TMAX
    		if m.isnan(tmin) or m.isnan(tmax):
    			continue
    		result.ix[yy_mm].ndays += 1
    		result.ix[yy_mm].SUM_TMIN += tmin
    		result.ix[yy_mm].SUM_TMAX += tmax

    	result['AVERAGE_TMIN'] = (result.SUM_TMIN*0.1) / result.ndays
    	result['AVERAGE_TMAX'] = (result.SUM_TMAX*0.1) / result.ndays
    	result['AVERAGE_TEMP'] = (result.AVERAGE_TMIN + result.AVERAGE_TMAX) * 0.5

    	return result



