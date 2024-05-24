from flask import Flask, jsonify, request
import requests
# from flask_cors import CORS

app = Flask(__name__)

# cors = CORS(app, resources={r"/api_vinfo/*": {"origins": "*"}})



def getChallan(vehNum):
  try:
    response = requests.get(
    f'https://www.carinfo.app/_next/data/MuceL2U-BNrimc0ehV-rh/challan-details/{vehNum}.json'
    )
    data  = response.json()
    header_element = data['pageProps']['challanDetailsResponse']['data']['headerElement']
    challans =  data['pageProps']['challanDetailsResponse']['data']['challans']
    return header_element, challans
  except requests.exceptions.RequestException as e:
    print("Error making the request:", e)
  except ValueError as e:
    print("Error parsing JSON response:", e)


def get_ekey(vehnum):
  headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer':
    'https://www.acko.com/car-journey/car-number?cardType=car-number',
    'Content-Type': 'application/json',
    'x-landing-path': '/lp/new-comprehensive',
    'x-landing-url':
    'https://www.acko.com/car-journey/car-number?cardType=car-number',
    'Origin': 'https://www.acko.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
  }

  json_data = {
    'registration_number': vehnum,
    'phone': '',
    'origin': 'acko',
    'product': 'car',
    'is_new': False,
  }

  response = requests.post(
    'https://www.acko.com/motororchestrator/api/v2/proposals',
    # cookies=cookies,
    headers=headers,
    json=json_data,
  )

  return response.json()['ekey']


def get_vehicle_details(vehnum):
  try:
    response = requests.get(
      f'https://www.acko.com/motororchestrator/api/v2/proposals/{get_ekey(vehnum)}',
    )
    return response.json()
  except:
    return "no"



# CORS(app)



@app.route('/')
def index():
    return 'Hello you can visit to use example of these api https://vehcileapi.vercel.app/DL8CX5463  '

@app.route('/about')
def about():
    return 'About'
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
    onwer_name=""
    # Prepare the response data
    if get_vehicle_details(vehNum) != "no":
      vdata=get_vehicle_details(vehNum)
      onwer_name = vdata['user']['name']
      data = vdata['vehicle']
    response_data = {
      'vehNum': number,
      'onwer_name': onwer_name,
      'header_element': header_element,
      'challans': challans,
      'vehicleDetails': data
    }

    # Create the response with CORS headers
    response = jsonify(response_data)
    # response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
