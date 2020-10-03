# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:45:53 2020

@author: tony51307
"""

def find_places_from_text(place_name, api_key, language):
    inputtype = 'textquery'
    url = ('https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
            '?key=%s'
            '&inputtype=%s'
            '&input=%s'
          '&language=%s') % (api_key, inputtype, place_name, language)
    response = requests.get(url)
    jsonData = response.json()
    id_list = []
    for i in jsonData['candidates']:
        id_list.append(i['place_id'])
    # return a list of place IDs
    return id_list

