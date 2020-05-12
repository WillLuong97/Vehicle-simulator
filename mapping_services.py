import requests
import math
import json
import urllib.parse

# Documentation for address formatting:
# https://docs.mapbox.com/help/troubleshooting/address-geocoding-format-guide/

# Documentation for direction api errors:
# https://docs.mapbox.com/api/navigation/#directions-api-errors


class Mapping_Services:
    accessToken = "pk.eyJ1Ijoid2lsbGx1b25nOTciLCJhIjoiY2s2bno3OTNvMGRnaTNqcGJzOG9jY2N2ZiJ9.HfvhKBvZreCaO8KFqlYkRw"
    MIN_STOPS = 2
    MAX_STOPS = 25
    
    def __init__ (self, stops=[]):
        self.stops = stops
        self.directions = None
    
    # get stops
    @property
    def stops (self):
        return self._stops
    
    # setting the stops, checks the length for stops
    @stops.setter
    def stops (self, stops):
        # Error handling for stops
        if len(stops) < self.MIN_STOPS:
            raise Exception ("Not enough stops! Need at least " + str(self.MIN_STOPS) + "! Length of stops is " + str(len(stops)))
        if len(stops) > self.MAX_STOPS:
            raise Exception ("Too many stops! Limit is " + str(self.MAX_STOPS) + "! Length of stops is " + str(len(stops)))

        self._stops = stops
        
    # translate each stop into coordinates        
    def get_coordinates(self, stops, country="US"):
        # initialize list of coordinates from stops
        stops_coordinates = list()
        for stop in stops:
            coordinates = self.get_address_lat_long (stop, country)
            stops_coordinates.append ({"address": stop, "coordinates": coordinates})
        
        return stops_coordinates

    # get the coordinates of an address using a geocoder
    def get_address_lat_long(self, address, country="US"):
        # parse the address into a url encoded form
        parsed_address = self.parse_address_into_url (address)
        
        # construct the url with the address and access token
        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+ parsed_address + ".json?country=" + country + "&access_token=" + self.accessToken
        print ("get_address:", url)

        # GET Request to Mapbox for the latitude and long
        response = requests.get(url)
        response.close()
        json_object = response.json()
        
        # Grab the coordinates
        coordinates = json_object['features'][0]['geometry']['coordinates']
        return coordinates
    
    # turn an address string into a url encoded string for API calls
    def parse_address_into_url (self, address):
        address = address.replace(',', '')
        return urllib.parse.quote(address)
    
    # get a directions object that goes through each stop
    def get_directions (self):
        url = 'https://api.mapbox.com/directions/v5/mapbox/driving/'
        stop_coordinates = self.get_coordinates(self.stops)
        for i in range(len(stop_coordinates)):
            coordinates = stop_coordinates[i]["coordinates"]
            url += str(coordinates[0]) + ',' + str(coordinates[1])
            
            # if more stops are available, add a semicolon
            if i+1 < len(stop_coordinates):
                url += ';'
        url += '?steps=true&geometries=geojson&access_token=' + self.accessToken;
        print ("get_directions:",url)
        
        # send the get request to Mapbox
        response = requests.get(url)
        response.close()
        directions = response.json()
        
        if directions["code"] != "Ok":
            raise Exception("Could not retrieve directions! " + directions["message"])
        
        self.directions = Route(directions)
        return self.directions

# Mapbox route object API
# https://docs.mapbox.com/api/navigation/#route-object

class Route:
    def __init__(self, directions):
        self._directions = directions

    # get the json response from Mapbox's directions API
    @property
    def directions(self):
        return self._directions
    
    # get the legs
    # https://docs.mapbox.com/api/navigation/#route-leg-object
    @property
    def legs (self):
        return self.directions["routes"][0]["legs"]

    # obtain the eta in minutes from directions
    @property
    def eta (self):
        eta = self.directions["routes"][0]['duration']
        
        # convert seconds into minutes
        if eta > 1:
            eta = math.ceil(eta/60)
        
        return eta
    
    # obtain the distance in meters from directions
    @property
    def distance (self):
        distance = self.directions["routes"][0]['distance']
       
        return distance

    # get the route optimized for drawing on a map
    @property
    def map_route_coordinates (self):
        return self.directions["routes"][0]["geometry"]["coordinates"]

    # get the route optimized for vehicle simulation
    @property
    def vehicle_route_coordinates (self):
        vehicle_route_coordinates = list()
        for leg in self.legs:
            for step in leg["steps"]:
                vehicle_route_coordinates.append(step["geometry"]["coordinates"])
        return vehicle_route_coordinates