import requests

response = requests.post(
    "http://127.0.0.1:5000/update-schemes",
    json={"url": "https://pmkisan.gov.in/"}
)

print(response.status_code)
print(response.text)