import datetime
import pandas as pd
import numpy as np
import temperature as tt

from pandas import DataFrame

class EtBlaneyCriddleModel:
    """Class that generates monthly ET estimates using Blaney-Criddle method"""

    def __init__(self):
        self.temperatureData = tt.GhcnTemperatureData()
        self.p = np.array([ [ 0.15, 0.20, 0.26, 0.32, 0.38, 0.41, 0.40, 0.34, 0.28, 0.22, 0.17, 0.13],
			 				[ 0.17, 0.21, 0.26, 0.32, 0.36, 0.39, 0.38, 0.33, 0.28, 0.23, 0.18, 0.16],
							[ 0.19, 0.23, 0.27, 0.31, 0.34, 0.36, 0.35, 0.32, 0.28, 0.24, 0.20, 0.18],
							[ 0.20, 0.23, 0.27, 0.30, 0.34, 0.35, 0.34, 0.32, 0.28, 0.24, 0.21, 0.20],
							[ 0.22, 0.24, 0.27, 0.30, 0.32, 0.34, 0.33, 0.31, 0.28, 0.25, 0.22, 0.21],
							[ 0.23, 0.25, 0.27, 0.29, 0.31, 0.32, 0.32, 0.30, 0.28, 0.25, 0.23, 0.22],
							[ 0.24, 0.25, 0.27, 0.29, 0.31, 0.32, 0.31, 0.30, 0.28, 0.26, 0.24, 0.23],
							[ 0.24, 0.26, 0.27, 0.29, 0.30, 0.31, 0.31, 0.29, 0.28, 0.26, 0.25, 0.24],
							[ 0.25, 0.26, 0.27, 0.28, 0.29, 0.30, 0.30, 0.29, 0.28, 0.26, 0.25, 0.25],
							[ 0.26, 0.26, 0.27, 0.28, 0.29, 0.29, 0.29, 0.28, 0.28, 0.27, 0.26, 0.25],
							[ 0.26, 0.27, 0.27, 0.28, 0.28, 0.29, 0.29, 0.28, 0.28, 0.27, 0.26, 0.26],
							[ 0.27, 0.27, 0.27, 0.28, 0.28, 0.28, 0.28, 0.28, 0.28, 0.27, 0.27, 0.27],
							[ 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27]])
        self.north_lat = DataFrame(self.p, columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], index = range(60, -1, -5))
        self.south_lat = DataFrame(self.p, columns = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6], index =range(60, -1, -5))

    @staticmethod
    def idx(lat):
		n = int(abs(round(lat,-1)))
		r = n % 5
		if r == 0:
			return n
		if r >= 2.5:
			return n + (5-r)
		else:
			return n - r

    def compute(self, lat, lon, start_date, nDays):
    	# ToDo: ignore start_date - this should go to query
    	temp_df = self.temperatureData.get_data_as_df(lat, lon, nDays)
    	if temp_df is None:
    		return

    	result = tt.TemperatureData.monthly_temperature_aggregates(temp_df)
    	#  p (0.46 T mean +8
    	p_table = self.north_lat if lat > 0.0 else self.south_lat
    	p_lat = EtBlaneyCriddleModel.idx(lat)
    	p_table = p_table.ix[p_lat]
    	result['P_LAT'] = p_table[result.month].values
    	result['ET'] = result.P_LAT*((0.46 * result.AVERAGE_TEMP) + 8.0)
    	return result


