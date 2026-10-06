import requests

API_URL = "https://hackathon.api.qloo.com"
API_KEY = "hack_73913cf282adf18cb8c9efd647b5aa88d0138b97"

headers = {
    "x-api-key": API_KEY,
    "Accept": "application/json"
}

def test_search(query):
    url = f"{API_URL}/search"
    params = {"query": query} 
    response = requests.get(url, headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)

if __name__ == "__main__":
    test_search("The National")
