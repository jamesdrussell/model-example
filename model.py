import numpy as np

def test_function_1(request):
    a = np.array([1, 2, 3])
    return { 
        'message' : a.size
    }

def test_function_2(request):
    return { 
        'message' : request['name']
    }
