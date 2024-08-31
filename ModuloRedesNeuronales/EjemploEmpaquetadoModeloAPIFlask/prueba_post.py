import requests as req
import numpy as np


data = {
    'sl':4.7,
    'sw':3.2,
    'pl':1.3,
    'pw':0.2
}

url = 'http://localhost:5000/api/v0.0/predict'

headers = {'Content-Type': 'application/json'}

response = req.post(url, json=data, headers=headers)

print(response)
print(response.status_code)
print(response.json())




