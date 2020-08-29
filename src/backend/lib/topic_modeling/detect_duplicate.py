import requests
import json

URL = 'https://e3ba8a7e.ngrok.io'

def detect_duplicate(title1, doc1, title2, doc2):
	request_input = [[title1, doc1], [title2, doc2]]
	res = requests.post(URL, json={'text' : request_input})
	result = json.loads(res.text)
	return result
