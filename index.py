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
from helpers.get_recommendations import get_most_popular, get_product_recommendations

def path(file_name, path_name='static/'):
    return path_name+file_name

active_devices_df = pd.read_csv(path("ulta_beauty__makeup_&_skincare-active_devices-20190724-20191021.csv"), encoding = "ISO-8859-1")
store_details_df = pickle.loads(open(path('store_details.pickle'), 'rb').read())
sku_metadata_df = pd.read_csv(path("Sku_MetaData.csv"), encoding = "ISO-8859-1")
product_catalog_df = pd.read_csv(path('Product_Catalog.psv'), delimiter='|')
product_catalog_df['CATEGORY_NAME'] = product_catalog_df['CATEGORY_NAME'].astype('category')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/get_product_recommendation')
def get_recommendation():
    keyword = request.args.get("keyword", "lipstick")
    return jsonify(items=get_product_recommendations(keyword))

@app.route('/api/get_most_popular')
def get_popular():
    return jsonify(items=get_most_popular())

@app.route('/api/get_nearest_store')
def get_nearest_store():
    lat = float(request.args.get("lat", "0"))
    lng = float(request.args.get("lng", "0"))
    closest_row = closest_row_func((lat,lng), store_details_df).iloc[0,:]
    return closest_row.to_json(orient='index')

def calc_dist(point, row): 
    return distance.vincenty(point, (row['coordinates'][0], row['coordinates'][1])).km

def closest_row_func(point, gpd2):
    gpd2['Dist'] = gpd2['geometry'].apply(lambda row: calc_dist(point, row))
    min_distance = gpd2['Dist'].min()
    closest_row = gpd2[gpd2['Dist'] == min_distance]
    return closest_row

if __name__ == '__main__':
	app.run(debug=True, port=5000)