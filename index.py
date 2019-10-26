from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/get_product_recommendation')
def get_recommendation():
    keyword = request.args.get("keyword", "lipstick")
    return jsonify(items=get_product_recommendations(keyword))

def get_product_recommendations(keyword):
	return []

if __name__ == '__main__':
	app.run(debug=True, port=5000)