def test_function_1(request):
    return { 
        'message' : 'test function asdfasdfasdf!'
    }

def test_function_2(request):
    return { 
        'message' : request['name']
    }
