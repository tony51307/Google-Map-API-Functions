# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:17:07 2020

@author: tony51307
"""
import numpy as np
import requests

def getLatLng(addr, api_key, language):
    url = ('https://maps.googleapis.com/maps/api/geocode/json'
            '?address=%s'
            '&language=%s'
            '&key=%s') % (addr, language, api_key)
    response = requests.get(url)
    jsonData = response.json()
    results = jsonData['results']
    try:
        lat = results[0]['geometry']['location']['lat']
        lng = results[0]['geometry']['location']['lng']
        return (lat,lng)
    except:
        return np.nan