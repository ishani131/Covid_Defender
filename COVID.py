import requests, json
def get_values():
    url = "https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=truen"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = requests.request("GET", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    res = dict(json_data)
    return res

