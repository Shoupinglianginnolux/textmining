import requests as requests
import json as json

def CheckAD(userId, password):
   data = {"UserID": userId, "password": password}
   requests.adapters.DEFAULT_RETRIES = 5
   # response = requests.post("http://jnb2bws01/InxSSOAuth/api/Auth/CheckAD", json=data)
   response = requests.post(
       "http://inlcnws/InxSSOAuth/api/Auth/CheckAD",
       json=data,
       headers={"Connection": "close"},
   )
   json_data = json.loads(response.text)
   return json_data

   