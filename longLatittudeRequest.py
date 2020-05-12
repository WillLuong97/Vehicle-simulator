import requests
import math
import json

accessToken = "pk.eyJ1Ijoid2lsbGx1b25nOTciLCJhIjoiY2s2bno3OTNvMGRnaTNqcGJzOG9jY2N2ZiJ9.HfvhKBvZreCaO8KFqlYkRw"
def getLongAndLatOfStartingPoint(starting_address):
    #Formatting the address of the starting location
    split_string = starting_address.split(",")
    street = split_string[0].split(" ")
    city = split_string[1].strip()
    state = split_string[2].strip()
    unformatted_starting = ("%20".join(street), city, state)
    startingCoordinate = "%20".join(unformatted_starting)


    #api call to get the longtiude and lattitude of a particular address 
    #API call to get the starting address
    API_CALL_Starting = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+ startingCoordinate + ".json?country=US&access_token=pk.eyJ1Ijoid2lsbGx1b25nOTciLCJhIjoiY2s2bno3OTNvMGRnaTNqcGJzOG9jY2N2ZiJ9.HfvhKBvZreCaO8KFqlYkRw"
    
    #Turning an API response into a json object
    #longtitude and lattitude of the starting location.
    jsonResponse = requests.get(API_CALL_Starting).json()
    # print(jsonResponse)
    coordinate = jsonResponse['features'][0]['geometry']['coordinates']
    latitude = coordinate[0]
    longtitude = coordinate[1]
    location_starting = {"lat": latitude, "lon": longtitude}
    # print("Pickup location: " + starting_address + " has coordinates: " +str(location_starting))
    print("")
    return location_starting

# getLongAndLatOfStartingPoint("3001 S Congress Ave, Austin, TX")

def getLongAndLatOfEndingPoint(end_address):

    #formatting the address of the ending location
    split_string = end_address.split(",")
    street = split_string[0].split(" ")
    city = split_string[1].strip()
    state = split_string[2].strip()
    unformatted_dropoff= ("%20".join(street), city, state)
    endingCoordinate = "%20".join(unformatted_dropoff)

    API_CALL_Ending = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+ endingCoordinate + ".json?country=US&access_token=pk.eyJ1Ijoid2lsbGx1b25nOTciLCJhIjoiY2s2bno3OTNvMGRnaTNqcGJzOG9jY2N2ZiJ9.HfvhKBvZreCaO8KFqlYkRw"

    #Longtitude and lattitude of the ending location
    jsonObject = requests.get(API_CALL_Ending).json()
    coordinate = jsonObject['features'][0]['geometry']['coordinates']
    latitude = coordinate[0]
    longtitude = coordinate[1]
    location_ending = {"lat": latitude, "lon": longtitude}

    # print("Dropoff location: " + end_address + " has coordinates: " + str(location_ending))
    return location_ending

# getLongAndLatOfEndingPoint("8071 North Lamar BLVD, Austin, Texas")

def returnETA(pickupLocation, dropoffLocation):
    #Extracting the pickup and dropoff long and lat
    longLatOfPickup = getLongAndLatOfStartingPoint(pickupLocation)
    longLatOfDropOff = getLongAndLatOfEndingPoint(dropoffLocation)

    
    url ='https://api.mapbox.com/directions/v5/mapbox/driving/' + str(longLatOfPickup["lat"]) + ',' + str(longLatOfPickup["lon"]) + ';' + str(longLatOfDropOff["lat"]) + ',' + str(longLatOfDropOff["lon"]) + '?geometries=geojson&access_token=' + accessToken

    response = requests.get(url).json()
    # print(response)
    route = response['routes'][0]['geometry']['coordinates']
    print(route)

    retETA = response["routes"][0]['duration']
    # print(retETA)
    retETAInMinutes = math.ceil(retETA/60)
    retETAJSON = json.dumps({"eta": retETAInMinutes})
    print("")
    print(str(retETAJSON))
    return retETAJSON


returnETA("810 Guadalupe St, Austin, Tx", "3600 Presidential Blvd, Austin, TX")


