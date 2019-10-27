from flask import Flask, request, jsonify
app = Flask(__name__)
import config


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
    #address.split
    #https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,
    #+Mountain+View,+CA&key=YOUR_API_KEY
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address +'&key='+ config.API_KEY
    return None

def get_product_recommendations(keyword):
	return []


if __name__ == '__main__':
	app.run(debug=True, port=5000)