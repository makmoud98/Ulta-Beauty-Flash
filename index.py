from flask import Flask, request, jsonify
app = Flask(__name__)
import config
import pandas as pd
import geopandas as gpd
'''
path = 'static/'
store_hours_df = pd.read_csv(path+"Store_Hours.csv")
store_hours_df.info()

active_devices_df = pd.read_csv("ulta_beauty__makeup_&_skincare-active_devices-20190724-20191021.csv", encoding = "ISO-8859-1")
'''
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
    address = '+'.join(address.split(' '))
    #https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,
    #+Mountain+View,+CA&key=YOUR_API_KEY
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address +'&key='+ config.API_KEY
    print(url)
    return None

def get_product_recommendations(keyword):
	return []

#convert_address("1200 Journey")

if __name__ == '__main__':
	app.run(debug=True, port=5000)