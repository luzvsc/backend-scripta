import requests

url = 'http://127.0.0.1:8000/empresas/login'
data = {'email_contato': 'techsolutions@example.com', 'senha': 'password'}
try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

data2 = {'email': 'techsolutions@example.com', 'senha': 'password'}
try:
    response = requests.post(url, json=data2)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
