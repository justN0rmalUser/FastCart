import requests

data = {"key": "value", "number": 123}
response = requests.post('http://127.0.0.1:5000/data', json=data, headers={"Authorization": "662317420"})
print(response.json())