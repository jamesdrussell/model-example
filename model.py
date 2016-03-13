import numpy as np
import requests as req

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