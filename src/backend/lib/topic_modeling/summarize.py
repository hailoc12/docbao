import requests
import json

URL = 'https://e3ba8a7e.ngrok.io'

def summarize(text):
	res = requests.post(URL, json={'text' : text})
	result = json.loads(res.text)
	return result
