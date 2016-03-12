import fb_query;

def et_calc(request):
	client = fb_query.FbApi('ghcn')
	result = client.stations_by_radius_q(42.0347, -93.6200, 2, 100)
	print result
	return result.json()
