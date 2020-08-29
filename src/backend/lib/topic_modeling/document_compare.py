import requests
import json

URL = 'https://e3ba8a7e.ngrok.io'

def distance(text1, text2):
	res = requests.post(URL, json={'text' : [text1, text2]})
	result = json.loads(res.text)
	return result
