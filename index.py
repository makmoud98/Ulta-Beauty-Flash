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
store_details_joined_df = pickle.loads(open(path('store_details.pickle'), 'rb').read())
store_details_df = pickle.loads(open(path('store_details_join_hours.pickle'), 'rb').read())

sku_metadata_df = pd.read_csv(path("Sku_MetaData.csv"), encoding = "ISO-8859-1")
product_catalog_df = pd.read_csv(path('Product_Catalog.psv'), delimiter='|')
product_catalog_df['CATEGORY_NAME'] = product_catalog_df['CATEGORY_NAME'].astype('category')

store_inventory_df = pd.read_csv(path('Store_Inventory.csv'), encoding = "ISO-8859-1")

@app.route('/')
def hello_world():
    return 'hello_world'

@app.route('/api/get_product_recommendation')
def get_recommendation():
    keyword = request.args.get("keyword", "lipstick")
    return jsonify(items=get_product_recommendations(keyword))

@app.route('/api/get_nearest_store')
def get_nearest_store():
    lat = float(request.args.get("lat", "0"))
    lng = float(request.args.get("lng", "0"))
    closest_row = closest_row_func((lat,lng), store_details_df).iloc[0,:]
    return closest_row.to_json(orient='index')

@app.route('/api/get_in_store')
def get_in_store():
    sku_id = float(request.args.get("sku-id", "00000"))
    lat = float(request.args.get("lat", "0"))
    lng = float(request.args.get("lng", "0"))
    closest_rows = get_closest_stores((lat,lng), store_details_df)
    for index, row in closest_rows.iterrows():
        tmp = item_in_store(row['STORE_ID'], sku_id)
        if tmp.shape[0] > 0:
            return tmp.to_json(orient='index')
    return "[]"
    

#within 10 km
@app.route('/api/get_nearest_stores')
def get_nearest_stores():
    lat = float(request.args.get("lat", "0"))
    lng = float(request.args.get("lng", "0"))
    closest_rows = get_closest_stores((lat,lng), store_details_df)
    return closest_rows.to_json(orient='index')

#returns whether item in store
def item_in_store(store_id, sku_id):
    joined_df = store_inventory_df.merge(product_catalog_df, on=['SKU_ID'], how='inner')
    return joined_df[joined_df['Store_ID'] == store_id][joined_df['SKU_ID'] == sku_id]

def calc_dist(point, row): 
    return distance.vincenty(point, (row['coordinates'][0], row['coordinates'][1]))

def closest_row_func(point, gpd2):
    gpd2['Dist'] = gpd2['geometry'].apply(lambda row: calc_dist(point, row))
    min_distance = gpd2['Dist'].min()
    closest_row = gpd2[gpd2['Dist'] == min_distance]
    return closest_row

def get_closest_stores(point, gpd2):
    gpd2['Dist'] = gpd2['geometry'].apply(lambda row: calc_dist(point, row))
    sorted_gpd = gpd2.sort_values('Dist')
    closest_stores = sorted_gpd.head()
    closest_stores = closest_stores[closest_stores['Dist'] < 10]
    return closest_stores

@app.route('/api/get_most_popular')
def get_popular():
    return jsonify(items=get_most_popular())

if __name__ == '__main__':
	app.run(debug=True, port=5000)