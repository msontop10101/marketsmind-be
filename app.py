import requests

url = "https://schwab.p.rapidapi.com/news/get-details"

querystring = {"docID":""}

headers = {
	"X-RapidAPI-Key": "76a5157e15mshabb2b2da8cf05eap1e1d89jsnfa7b5878b987",
	"X-RapidAPI-Host": "schwab.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())