import requests

data = {
    "state": "Karnataka",
    "crop": "Rice",
    "land": 5,
    "category": "General",
    "income": 400000
}

res = requests.post("http://127.0.0.1:5000/recommend", json=data)
print(res.json())