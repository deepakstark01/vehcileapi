import requests

def getChallan(vehNum):
  url = f"https://web.cuvora.com/car/web/details/challan/?vehicleNum={vehNum}"
  # https://web.cuvora.com/car/web/details/challan/?vehicleNum=DL9CX5463
  headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "src": "car-info_web",
    "appVersion": "251",
    "deviceId": "36378a-d18d-3500-7b3b-35d30d35bb6",
    "userId": "64ba5cf67fc4493310ec330g",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site"
  }
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    header_element = response_data["data"]["headerElement"]
    challans = response_data["data"]["challans"]
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


@app.route('/', methods=['GET', 'POST'])
def index():
  return "Hey manish"


app.run(host='0.0.0.0', port=81)
