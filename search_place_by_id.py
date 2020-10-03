# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:37:32 2020

@author: tony51307
"""

import requests

def search_place_by_id(place_id,api_key,language):
    url = 'https://maps.googleapis.com/maps/api/place/details/json?key='+api_key+'&place_id='+ place_id+'&language='+language
    request = requests.get(url)
    data = request.json()
    # return a dictionary containing the details of the place
    return data