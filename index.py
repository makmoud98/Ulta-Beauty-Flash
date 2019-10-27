from flask import Flask, request, jsonify
app = Flask(__name__)
import config
import pandas as pd
import geopandas as gpd
import requests
import json
import pdb
import geopy.distance as distance
from shapely.ops import nearest_points
import pickle

def path(file_name, path_name='static/'):
    return path_name+file_name

def convert_address(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'key': config.API_KEY, 'address': '+'.join(address.split(' '))}
    r = requests.get(url, params)
    loc = json.loads(r.text)['results'][0]['geometry']['location']
    return {'type':'Point', 'coordinates': [loc['lat'], loc['lng']]}

store_hours_df = pd.read_csv(path("Store_Hours.csv"))
#store_hours_df.info()
active_devices_df = pd.read_csv(path("ulta_beauty__makeup_&_skincare-active_devices-20190724-20191021.csv"), encoding = "ISO-8859-1")
store_details_df = pickle.loads(open(path('new_product_details.txt'), 'rb').read())
sku_metadata_df = pd.read_csv(path("Sku_MetaData.csv"), encoding = "ISO-8859-1")
product_catalog_df = pd.read_csv(path("Product_Catalog.csv"), encoding = "ISO-8859-1", sep = "|")
product_catalog_df['CATEGORY_NAME'] = product_catalog_df['CATEGORY_NAME'].astype('category')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/get_product_recommendation')
def get_recommendation():
    keyword = request.args.get("keyword", "lipstick")
    return jsonify(items=get_product_recommendations(keyword))

df = pd.DataFrame(
    {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
     'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
     'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
     'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})

gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

pdb.set_trace()
def min_dist(point, gpd2):
    gdf['geometry'][0].coords.xy[0][0]
    gpd2['Dist'] = gpd2.apply(lambda row:  distance.vincenty(point, (row['geometry'][0].coords.xy[0][0], row['geometry'][0].coords.xy[1][0])))
    #gpd2['Dist'] = gpd2.apply(lambda row:  point.distance(row.geometry),axis=1)
    geoseries = gpd2.iloc[gpd2['Dist'].argmin()]
    return geoseries
min_dist((-58.66, -34.58), gdf)
#@app.route('/api/get_nearest_store')
def get_nearest_store(lat, lng):
    
    return None

def get_product_recommendations(keyword):
	return []

#convert_address("1200 Journey")

if __name__ == '__main__':
	app.run(debug=True, port=5000)