from django.core.cache import cache
from rest_framework import views, response
from rest_framework.response import Response
import requests
import os

class NewsView(views.APIView):
    def get(self, request):
        # Set cache key
        cache_key = 'news'
        # Try to get data from cache
        data = cache.get(cache_key)
        if not data:
            # Data not found in cache, make request to API
            url = "https://schwab.p.rapidapi.com/news/list-latest"
            headers = {
                "X-RapidAPI-Key": os.getenv('X_RAPIDAPI_KEY'),
                "X-RapidAPI-Host": "schwab.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            # Store data in cache for 6 hours
            cache.set(cache_key, data, 21600)
        return Response(data)


class GetDetailsView(views.APIView):
    def get(self, request):
        docID = request.query_params.get('docID')
        url = "https://schwab.p.rapidapi.com/news/get-details"
        querystring = {"docID": docID}
        headers = {
            "X-RapidAPI-Key": os.getenv('X_RAPIDAPI_KEY'),
            "X-RapidAPI-Host": "schwab.p.rapidapi.com"
        }
        res = requests.get(url, headers=headers, params=querystring)
        return response.Response(res.json())

