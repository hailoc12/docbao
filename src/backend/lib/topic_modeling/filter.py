import requests
import json

URL = 'https://e3ba8a7e.ngrok.io'

def detect_duplicate(content):
	res = requests.post(URL, json={'text' : content})
	result = json.loads(res.text) # True or False
	return result