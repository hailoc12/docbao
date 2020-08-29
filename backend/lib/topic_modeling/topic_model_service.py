import requests
import json

URL = 'http://103.192.236.77:2020'

def predict_topic(text):
	res = requests.post(URL, json={'text' : text})
	topic = json.loads(res.text)
	return topic

if __name__ == '__main__':
	txt = (predict_topic('Tao ở Hà Nội , và mới chuyển qua Hồ Chí Minh. à tiện tao tên là Nguyễn Huy Tuyển, số điện thoại của tao là 01223530692'))
	print(txt)
