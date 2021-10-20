import pandas as pd
import numpy as np
import requests
import time

class Address:
    def __init__(self,full_addr, country, city,area_level_1,area_level_2, zipcode):
        self.city = city
        self.country = country
        self.zip = zipcode 
        self.text = full_addr
        self.area_level_1 = area_level_1
        self.area_level_2 = area_level_2

    def set_full_addr(self, addr:str):
        self.text = addr
    
    def set_country(self, country:str):
        self.country = country

    def set_postCode(self, zipcode:str):
        self.zip = zipcode

    def set_city(self, city:str):
        self.city = city

    def set_area_level_1(self, area_level_1:str):
        self.area_level_1 = area_level_1

    def set_area_level_2(self, area_level_2:str):
        self.area_level_2 = area_level_2

class Place:
    def __init__(self,addr,lat,lng, phone, name, ID,business_status,open_time):
        self.address = addr
        self.lat = lat
        self.lng = lng
        self.phone = phone
        self.name = name
        self.id = ID
        self.business_status = business_status
        self.open_time = open_time

    def set_name(self, name:str):
        self.name = name

    def set_latlng(self, lat:str, lng:str):
        self.lat = lat
        self.lng = lng
        
class gmap:

    def __init__(self):
        self.api_key = ""
        self.language = "EN" 

    def setKey(self, key:str):
        self.api_key = key

    def setLanguage(self, languageCode:str):
        self.language = languageCode

    def find_places_from_text(self, place_name:str):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")

        inputtype = 'textquery'
        url = ('https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
                '?key=%s'
                '&inputtype=%s'
                '&input=%s'
            '&language=%s') % (self.api_key, inputtype, place_name, self.language)
        response = requests.get(url)
        jsonData = response.json()
        id_list = []
        for i in jsonData['candidates']:
            id_list.append(i['place_id'])
        # return a list of place IDs
        return id_list

    def getLatLng(self, addr: str):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        url = ('https://maps.googleapis.com/maps/api/geocode/json'
                '?address=%s'
                '&language=%s'
                '&key=%s') % (addr, self.language, self.api_key)
        response = requests.get(url)
        jsonData = response.json()
        results = jsonData['results']
        try:
            lat = results[0]['geometry']['location']['lat']
            lng = results[0]['geometry']['location']['lng']
            return (lat,lng)
        except:
            return (np.nan, np.nan)

    def getPostCode(self, addr:str):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        url = ('https://maps.googleapis.com/maps/api/geocode/json'
                '?address=%s'
                '&language=%s'
                '&key=%s') % (addr, self.language, self.api_key)
        response = requests.get(url)
        jsonData = response.json()
        results = jsonData['results']
        try:
            postCode = results[0]['address_components'][-1]['short_name']
            return postCode
        except:
            return np.nan

    def search_place_by_id(self, place_id:str):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        url = 'https://maps.googleapis.com/maps/api/place/details/json?key='+self.api_key+'&place_id='+ place_id+'&language='+self.language
        request = requests.get(url)
        data = request.json()
        # return a dictionary containing the details of the place
        business_status = data['result']['business_status']
        formatted_address = data['result']['formatted_address']
        international_phone = data['result']['international_phone_number']
        name = data['result']['name']
        open_time = data['result']['opening_hours']['weekday_text']
        ID = data['result']['place_id']
        address_components = data['result']['address_components']
        country = ""
        city = ""
        zipcode = ""
        area_level_1 = ""
        area_level_2 = ""
        for i in address_components:
            if 'country' in i['types']:
                country = i['long_name']
            elif 'administrative_area_level_3' in i['types']:
                area_level_2 = i['long_name']
            elif 'administrative_area_level_2' in i['types']:
                area_level_1 = i['long_name']
            elif 'administrative_area_level_1' in i['types']:
                city = i['long_name']
            elif 'postal_code' in i['types']:
                zipcode = i['long_name']
        addr = Address(formatted_address,country,city,area_level_1,area_level_2,zipcode)
        lat = data['result']['geometry']['location']['lat']
        lng = data['result']['geometry']['location']['lng']
        place = Place(addr,lat,lng,international_phone,name,ID,business_status,open_time)
        return place

    # destin_LatLng needs to be input in the string form "[Lat], [Lng]"
    def getDistance_by_placeID(self, orign_placeId:str, dest_placeId:str,mode="driving"):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        if mode not in ['driving','walking','bicycling','transit']:
            raise Exception('Mode is only availble as followings: ["driving","walking","bicycling","transit"]')
        ## Calculate the distance between two points on Google Map ##
        url = ('https://maps.googleapis.com/maps/api/distancematrix/json'
            '?origins=place_id:%s'
            '&destinations=place_id:%s'
            '&language=%s'
            '&key=%s'
            '&mode=%s') % (orign_placeId,dest_placeId, self.language, self.api_key,mode)
        response = requests.get(url)
        jsonData = response.json()
        distance = jsonData['rows'][0]['elements'][0]['distance']['value']
        return int(distance)

    def getDistance_by_latlng(self,lat1,lng1,lat2,lng2,mode="walking"):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        if mode not in ['driving','walking','bicycling','transit']:
            raise Exception('Mode is only availble as followings: ["driving","walking","bicycling","transit"]')
        ## Calculate the distance between two points on Google Map ##
        url = ('https://maps.googleapis.com/maps/api/distancematrix/json'
            '?origins=%s'
            '&destinations=%s'
            '&language=%s'
            '&key=%s'
            '&mode=%s') % (lat1+", "+lng1,lat2+", "+lng2, self.language, self.api_key,mode)
        response = requests.get(url)
        jsonData = response.json()
        distance = jsonData['rows'][0]['elements'][0]['distance']['value']
        return int(distance)

    def getDistance_by_address(self,addr1,addr2,mode="driving"):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        if mode not in ['driving','walking','bicycling','transit']:
            raise Exception('Mode is only availble as followings: ["driving","walking","bicycling","transit"]')
        ## Calculate the distance between two points on Google Map ##
        url = ('https://maps.googleapis.com/maps/api/distancematrix/json'
            '?origins=%s'
            '&destinations=%s'
            '&language=%s'
            '&key=%s'
            '&mode=%s') % (addr1, addr2, self.language, self.api_key,mode)
        response = requests.get(url)
        jsonData = response.json()
        distance = jsonData['rows'][0]['elements'][0]['distance']['value']
        return int(distance)

    def nearbySearch(self, addr:str, place_type:str, distance:float):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        # Get Lat Lng for the centered place
        lat, lng = self.getLatLng(addr)
        url = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
            '?location=%s'
            '&radius=%s'
            '&type=%s'
            '&language=%s'
            '&key=%s') % (str(lat)+','+str(lng),str(distance),place_type, self.language, self.api_key)
        response = requests.get(url)
        time.sleep(2)
        jsonData = response.json()
        results = jsonData['results']
        dic_list = []
        for r in results:
            dist = self.getDistance_by_address(r['formatted_address'],addr)
            if dist<=distance:
                dic = dict()
                dic['Name'] = r['name']
                dic['Place_Id'] = r['place_id']
                dic['Type'] = r['types']
                dic_list.append(dic)
        
        while 'next_page_token' in list(jsonData.keys()):
            nextPage = jsonData['next_page_token']
            url = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
            '?key=%s'
            '&pagetoken=%s') % (self.api_key,nextPage)
            response = requests.get(url)
            time.sleep(2)
            jsonData = response.json()
            results = jsonData['results']
            for r in results:
                dist = self.getDistance_by_address(r['formatted_address'],addr)
                # To confirm the distance is indeed within the required length
                if dist<=distance:
                    dic = dict()
                    dic['Name'] = r['name']
                    dic['Place_Id'] = r['place_id']
                    dic['Type'] = r['types']
                    dic_list.append(dic)
        return dic_list

    def get_travel_time_by_LatLng(self, lat1:str, lng1:str, lat2:str, lng2:str, mode='driving'):
        if self.api_key == "":
            raise Exception("Sorry, no api key set")
        if mode not in ['driving','walking','bicycling','transit']:
            raise Exception('Mode is only availble as followings: ["driving","walking","bicycling","transit"]')
        latlng1 = str(lat1)+', '+str(lng1)
        latlng2 = str(lat2)+', '+str(lng2)
        url = ('https://maps.googleapis.com/maps/api/distancematrix/json?'
            'key=%s'
            '&language=%s'
            '&origins=%s'
            '&destinations=%s'
            '&mode=%s') % (self.api_key,self.language,latlng1,latlng2,mode)
        response = requests.get(url)
        time.sleep(2)
        jsonData = response.json()
        duration = jsonData['rows'][0]['elements'][0]['duration']['text']
        return duration      

    def get_travel_time_by_address(self, address1:str, address2:str, mode='driving'):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        if mode not in ['driving','walking','bicycling','transit']:
            raise Exception('Mode is only availble as followings: ["driving","walking","bicycling","transit"]')
        lat1, lng1 = self.getLatLng(address1)
        lat2, lng2 = self.getLatLng(address2)
        latlng1 = str(lat1)+', '+str(lng1)
        latlng2 = str(lat2)+', '+str(lng2)
        url = ('https://maps.googleapis.com/maps/api/distancematrix/json?'
            'key=%s'
            '&language=%s'
            '&origins=%s'
            '&destinations=%s'
            '&mode=%s') % (self.api_key,self.language,latlng1,latlng2,mode)
        response = requests.get(url)
        time.sleep(2)
        jsonData = response.json()
        duration = jsonData['rows'][0]['elements'][0]['duration']['text']
        return duration

    def get_travel_time_by_place(self, place1:Place, place2:Place, mode='driving'):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        if mode not in ['driving','walking','bicycling','transit']:
            raise Exception('Mode is only availble as followings: ["driving","walking","bicycling","transit"]')
        lat1 = place1.lat
        lng1 = place1.lng
        lat2 = place2.lat
        lng2 = place2.lng
        latlng1 = str(lat1)+', '+str(lng1)
        latlng2 = str(lat2)+', '+str(lng2)
        url = ('https://maps.googleapis.com/maps/api/distancematrix/json?'
                'key=%s'
                '&language=%s'
                '&origins=%s'
                '&destinations=%s'
                '&mode=%s') % (self.api_key,self.language,latlng1,latlng2,mode)
        response = requests.get(url)
        time.sleep(2)
        jsonData = response.json()
        duration = jsonData['rows'][0]['elements'][0]['duration']['text']
        return duration
    
    def getAddress(self, lat:str, lng:str):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        url = ('https://maps.googleapis.com/maps/api/geocode/json?'
            'key=%s'
            '&language=%s'
            '&latlng=%s') % (self.api_key,self.language,str(lat)+','+str(lng))
        response = requests.get(url)
        time.sleep(2)
        jsonData = response.json()
        addr = jsonData['results'][0]['formatted_address']
        address_components = jsonData['results'][0]['address_components']
        country = ""
        city = ""
        zipcode = ""
        area_level_1 = ""
        area_level_2 = ""
        for i in address_components:
            if 'country' in i['types']:
                country = i['long_name']
            elif 'administrative_area_level_3' in i['types']:
                area_level_2 = i['long_name']
            elif 'administrative_area_level_2' in i['types']:
                area_level_1 = i['long_name']
            elif 'administrative_area_level_1' in i['types']:
                city = i['long_name']
            elif 'postal_code' in i['types']:
                zipcode = i['long_name']
        addr = Address(addr,country,city,area_level_1,area_level_2,zipcode)
        return addr

    def decompose_address(self, addr:str):
        if self.api_key == "":
            raise Exception("Sorry, no api key is set")
        url = ('https://maps.googleapis.com/maps/api/geocode/json'
                '?address=%s'
                '&language=%s'
                '&key=%s') % (addr, self.language, self.api_key)
        response = requests.get(url)
        jsonData = response.json()
        results = jsonData['results']
        country = ""
        city = ""
        zipcode = ""
        area_level_1 = ""
        area_level_2 = ""
        try:
            address_components = results[0]['address_components']
            address = results[0]['formatted_address']
            for i in address_components:
                if 'country' in i['types']:
                    country = i['long_name']
                elif 'administrative_area_level_3' in i['types']:
                    area_level_2 = i['long_name']
                elif 'administrative_area_level_2' in i['types']:
                    area_level_1 = i['long_name']
                elif 'administrative_area_level_1' in i['types']:
                    city = i['long_name']
                elif 'postal_code' in i['types']:
                    zipcode = i['long_name']
            return Address(address,country,city,area_level_1,area_level_2,zipcode)
        except:
            return np.nan
