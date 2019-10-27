from flask import Flask, request, jsonify
app = Flask(__name__)
import config
import pandas as pd
import geopandas as gpd
import requests
import json

def path(file_name, path_name='static/'):
    return path_name+file_name

store_hours_df = pd.read_csv(path("Store_Hours.csv"))
#store_hours_df.info()
active_devices_df = pd.read_csv(path("ulta_beauty__makeup_&_skincare-active_devices-20190724-20191021.csv"), encoding = "ISO-8859-1")
store_details_df = pd.read_csv(path("Store_Details.csv"), encoding = "ISO-8859-1")
sku_metadata_df = pd.read_csv(path("Sku_MetaData.csv"), encoding = "ISO-8859-1")
product_catalog_df = pd.read_csv(path("Product_Catalog.csv"), encoding = "ISO-8859-1", sep = "|")
product_catalog_df['CATEGORY_NAME'] = product_catalog_df['CATEGORY_NAME'].astype('category')

store_details_df['address']=store_details_df['ADDRESS_1']+', '+store_details_df['ADDRESS_2']+' ' + store_details_df['CITY']+' '+store_details_df['STATE']+' ' + str(store_details_df['ZIPCODE'])

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/get_product_recommendation')
def get_recommendation():
    keyword = request.args.get("keyword", "lipstick")
    return jsonify(items=get_product_recommendations(keyword))

@app.route('/api/get_nearest_store')
def get_nearest_store():
    return None

def convert_address(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'key': config.API_KEY, 'address': '+'.join(address.split(' '))}
    r = requests.get(url, params)
    loc = json.loads(r.text)['results'][0]['geometry']['location']
    return {'geometry':{'type':'Point', 'coordinates': [loc['lat'], loc['lng']]}}

def get_product_recommendations(keyword):
	return []

#convert_address("1200 Journey")

if __name__ == '__main__':
	app.run(debug=True, port=5000)