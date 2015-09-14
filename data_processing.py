
import pandas as pd
import ast
import json
import requests 
import math

INVALID_VALUE = 'Invalid_Value'

def convert_col_to_dict(x):
	try:
		return ast.literal_eval(x)
	except Exception as e:
		#TODO: Come back to this (around 15% user values are invalid)
		return INVALID_VALUE

def add_col_location(x):
	if 'geo' not in x or type(x['geo']) == float:
		bbox = x['place']['bounding_box']['coordinates'][0]
		lng = (bbox[0][0]+bbox[2][0])/2 
		lat = (bbox[0][1]+bbox[1][1])/2
		location = (lat, lng)
		print 'From Bounding Box: '+str(location)
	else:
		geo = ast.literal_eval(x['geo'])
		location = (geo['coordinates'][0], geo['coordinates'][1])
		print 'Already a point: '+str(location)
	return location

data = pd.read_csv('makkah_data_processed.csv', header=0, index_col=0)

data['user'] = data['user'].apply(convert_col_to_dict)
data = data[data['user'] != INVALID_VALUE]

data['place'] = data['place'].apply(convert_col_to_dict)
data['location'] = data.apply(add_col_location, axis=1)

data['screen_name'] = data['user'].apply(lambda x:x['screen_name']) 

export_data = data[['screen_name', 'location', 'loc_time']]
