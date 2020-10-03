# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:25:03 2020

@author: tony51307
"""

import numpy as np
import requests


def getPostCode(addr, api_key, language):
    url = ('https://maps.googleapis.com/maps/api/geocode/json'
            '?address=%s'
            '&language=%s'
            '&key=%s') % (addr, language, api_key)
    response = requests.get(url)
    jsonData = response.json()
    results = jsonData['results']
    try:
        postCode = results[0]['address_components'][-1]['short_name']
        return postCode
    except:
        return np.nan