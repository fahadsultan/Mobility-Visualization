
import pandas as pd
import ast
import json
import requests 

vis_data = pd.read_json('visualization_data.json')

vis_data.sort('loc_time')

REQUEST_URL_BASIC = "https://maps.googleapis.com/maps/api/directions/json?"

KEY = 'AIzaSyCpHbZc8tRVUNzEIBCq1qLN39jhLcYdP0E'
vis_data['path'] = ''

last_location = {}

def km_distance_between_two_points(point_one, point_two):
	# point_one = point_one[1:-1].split(', ')
	# point_two = point_two[1:-1].split(', ')
	return haversine(point_one[0], point_one[1], point_two[0], point_two[1])


def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    km = 6367 * c
    return km

for i in range(0, len(vis_data)):

	print i

	row = vis_data.iloc[i]
	if row['screen_name'] in last_location and km_distance_between_two_points(last_location[row['screen_name']], row['location']) > 0.5:
		origin = last_location[row['screen_name']]
		destination = row['location']

		print str(origin)+' to '+str(destination)
		params_str = 'origin='+str(tuple(origin))+"&destination="+str(tuple(destination))

		response =requests.get(REQUEST_URL_BASIC+params_str+'&key='+KEY)
		response = json.loads(response.content)
		if len(response['routes']) > 0:
			legs = response['routes'][0]['legs']
			path = []
			for leg in legs:
				steps = leg['steps']
				print len(steps)
				for step in steps:
					path.append({'x1':step['start_location']['lat'], 'y1':step['start_location']['lng'], 'x2':step['end_location']['lat'], 'y2':step['end_location']['lng']})

			vis_data.set_value(i, 'path', path)
		else:
			print response['status']
	
	last_location[row['screen_name']] = row['location']