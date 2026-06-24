import urllib.request
import json

url = 'http://127.0.0.1:8000/coordenadores/login'
data = json.dumps({'email': 'coordenacao@example.com', 'senha': '123456'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        print("Body:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("Erro HTTP:", e.code)
    print("Resposta erro:", e.read().decode('utf-8'))
except Exception as e:
    print("Erro:", e)
