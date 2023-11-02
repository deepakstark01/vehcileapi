from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from main import getChallan, get_vehicle_details
app = Flask(__name__)
cors = CORS(app, resources={r"/api_vinfo/*": {"origins": "*"}})

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'


# CORS(app)
@app.route('/<string:vehNum>', methods=['GET', 'POST'])
def home(vehNum):
  if request.method == 'GET':
    # vehNum = request.args.get('vehNum')
    if not vehNum:
      return jsonify(
        {"error":
         "Please provide a vehicle Number in the request query."}), 400
    number = vehNum.upper()
    header_element, challans = getChallan(number)
    data=""
    # Prepare the response data
    if get_vehicle_details(vehNum) != "no":
      data=get_vehicle_details(vehNum) 
    response_data = {
      'vehNum': number,
      'header_element': header_element,
      'challans': challans,
      'vehicleDetails': data
    }

    # Create the response with CORS headers
    response = jsonify(response_data)
    # response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
