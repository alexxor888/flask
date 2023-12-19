import requests

response = requests.post(
    "http://127.0.0.1:5000/hello/world?name=Alex&age=20",
    json={
        "country": "Russia",
        "city": "Moscow"
    },
    headers={"token": "123456"}
)

print(response.status_code)
print(response.text)