import pandas as pd
import numpy as np
import requests as req

import et
import time

def verify_et_compute():
    start = time.time()
    result = et_compute({"lat":42.021389, "lon":-93.77388, "days" : 365, "start-date" : "2012-01-01"})
    end = time.time()
    print (end-start)

def et_compute(request):
    lat = request['lat']
    lon = request['lon']
    ndays = request['days']
    etmodel = et.EtBlaneyCriddleModel()
    data_series = etmodel.compute(lat, lon, None, ndays)
    return pd.Series.to_dict(data_series['ET'])

def test_function_1(request):
    a = np.array([1, 2, 3])
    return { 
        'message' : a.size
    }

def test_function_2(request):
    a = req.get('https://api.farmbase.io/datasets/ghcn/stations?keys=station_id,min_date&limit=10')
    return { 
        'message' : a.json()
    }
