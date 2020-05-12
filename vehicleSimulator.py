#*********************************************FOR QA REVIEWERS: THE BACKEND SERVER IS UNDERGOING SOME MAJOR CHANGES AT THE MOMENT, PLEASE DON'T RUN THESE CODES AS IT MIGHT INTERFERE WITH THE SERVER MAINTENECE**********************************
#Vehicle simulator 
#FUNCTION: This python file will simulate a vehicle model that would interact with the Supply Back End server through a heartbeat signal relationship.
#Basic Postman documentation for API call to get vehicle information from the database
#https://documenter.getpostman.com/view/10366155/SzS4RT25?version=latest
import json
import requests
import threading
from threading import Thread
import os
import time
import random
from datetime import datetime
import math
from mapping_services import Mapping_Services




duration = time.perf_counter()

#Default location that each vehicle will be at
DEFAULT_LAT_STARTING = 30.390346000000008
DEFAULT_LONG_STARTING = -97.72559445767246
DEFAULT_VEHICLE_LOCATION = [DEFAULT_LONG_STARTING, DEFAULT_LAT_STARTING]
route_1 = [[-97.734955, 30.267914], [-97.736496, 30.268345], [-97.736839, 30.267427], [-97.734688, 30.266827], [-97.735077, 30.265757], [-97.735298, 30.264139], [-97.736923, 30.260164], [-97.737282, 30.257853], [-97.735046, 30.246187], [-97.735092, 30.24464], [-97.735664, 30.243183], [-97.742348, 30.231962], [-97.744484, 30.228928], [-97.747742, 30.22353], [-97.74897, 30.224411], [-97.75412, 30.226749], [-97.753044, 30.228733]]
route_2 = [[-97.711296, 30.348373], [-97.71151, 30.348476], [-97.709641, 30.35033], [-97.709167, 30.350809], [-97.710136, 30.35029], [-97.712341, 30.348577], [-97.712654, 30.348604], [-97.712715, 30.348749], [-97.714539, 30.353548], [-97.719604, 30.369637], [-97.740005, 30.381096], [-97.745453, 30.390524], [-97.746384, 30.393684], [-97.745003, 30.409201], [-97.747856, 30.422861], [-97.776642, 30.437927], [-97.788521, 30.445698], [-97.796989, 30.46892], [-97.804619, 30.484921], [-97.802254, 30.493267], [-97.804077, 30.498743], [-97.807228, 30.50198], [-97.811813, 30.503494], [-97.812706, 30.504841], [-97.82, 30.504711], [-97.831047, 30.500057], [-97.840248, 30.493916], [-97.844048, 30.497522], [-97.845604, 30.495325], [-97.846413, 30.495741], [-97.846786, 30.49514]]
route_3 = [[-97.745583, 30.271933], [-97.745239, 30.271835], [-97.747971, 30.264351], [-97.747711, 30.263622], [-97.749329, 30.259733], [-97.74353, 30.253229], [-97.736168, 30.248087], [-97.735779, 30.24799], [-97.735329, 30.245174], [-97.736061, 30.243069], [-97.736946, 30.241161], [-97.737152, 30.240694], [-97.742348, 30.231962], [-97.746643, 30.22471], [-97.750023, 30.219261], [-97.750626, 30.217573], [-97.749535, 30.216143], [-97.742958, 30.215986], [-97.710022, 30.212252], [-97.692719, 30.217714], [-97.684662, 30.221289], [-97.679741, 30.222427], [-97.675331, 30.22159], [-97.662727, 30.215014], [-97.660843, 30.213661], [-97.659782, 30.213104], [-97.659592, 30.212263], [-97.660645, 30.211428], [-97.662041, 30.211096], [-97.66259, 30.21151], [-97.665001, 30.209602], [-97.664764, 30.209044]]

DEFAULT_VEHICLE_STATUS = 'AVAILABLE'
warehouse_longHorn = [-97.73472238641511, 30.28464596553485]
vehicleID = "5e701c2eb15e7c5673d3f0b3"
vehicleID_2 = "5e7bdb2a93b142e5c8f1c123"
vehicleID_3 = "5e7bdb2c93b142e5c8f1c127"



# class Vehicle:
#     #Initializing attributes of a vehicle:
#     def __init__(self, vID, vName, vStatus):
#         self.vehicle_ID = vID
#         self.vechicle_Name = vName
#         self.vehicle_Status = vStatus

#Creating an intsance of a class:
# car1 = Vehicle(12345635, "Corola", "Idle")

# # A dictionary to store all information about the vehicle from the class
# vehicle_dictionary = {'ID': car1.vehicle_ID,
#                       'Name': car1.vechicle_Name,
#                       'Status': car1.vehicle_Status
# 


#Default location that each vehicle will be at
DEFAULT_LAT_STARTING = 30.390346000000008
DEFAULT_LONG_STARTING = -97.72559445767246
DEFAULT_COORDINATES_STRING = [[-97.734955, 30.267914], [-97.736496, 30.268345], [-97.736839, 30.267427], [-97.734688, 30.266827], [-97.735077, 30.265757], [-97.735298, 30.264139], [-97.736923, 30.260164], [-97.737282, 30.257853], [-97.735176, 30.246897], [-97.735489, 30.24427], [-97.741653, 30.23385], [-97.746803, 30.236261], [-97.750893, 30.237219], [-97.753571, 30.238791], [-97.756897, 30.234873], [-97.757393, 30.235142]]
#Main program that run the vsim
def main():
    #menu with options for vsim control.
    print("Welcome to the Vehicle Simulation Demonstrator")

    testCases = testCases = {1: 'Display all vehicle',
               2: 'Remove a vehicle',
               3: ' Begin Heartbeat',
               4: 'Create a vehicle',
               5: 'Heartbeat Disable',
               6: 'Future',
               7: 'Future',
               99: 'Exit this menu'}


    userInput(testCases)


# Asking user input for an options
# userChoices is a dictionary, key pointrs to test case
# Includes user input exception handling
# Loop until the user input is '99'
def userInput(userChoices):

    while True:
        print(' your choices'.upper(), '\t\t\tTest Case\n'.upper(), '-' * 55)

        #Looping through the values in the test case dictionary:
        for key, value in userChoices.items():
            print('\t', key, ' \t\t\t\t', value)
        try:
            choice = int(input("\nPlease enter the numeric choice for an option here: \n\t --> ".upper()))
        # Error handling
        except:
            print("\n********Something went wrong, please enter a numeric value***********\n")
            continue

        if choice == 99:
            print("**************Program Ended****************")
            print("")
            break

        menuExcept(choice)


# Map user selection (parameter) to module(function call)
def menuExcept(choice):

    #Pulling a displaying all vehicle currently stored in the server database
    #Making a REST request to the supply server for a full extensive live of all vehicles currently stored in the database
    #and display them nicely to the terminal console
    if choice == 1:
        displayVehicle()

    #Removing a veicle from the vsim.
    #----Still under development-------
    elif choice == 2:
        print("**********Removing a vehicle from the VSIM***************")
        print("")
        print("Here are the current vehicle in the VSIM: ")

        # Requesting to add all vehicle from the database into the local vsim.
        API_Call = 'https://supply.team12.softwareengineeringii.com/api/backend?vehicle-all=1'
        print('\tThe API http string --> ' + API_Call)
        print("")
        jsonResponse = requests.get(API_Call).json()
        #Converting the json object into a string:
        vehilceObjectTransfer = json.dumps(jsonResponse)
        #converting the string into a JSON object:
        vehicleDictForRemoving = json.loads(vehilceObjectTransfer)

        print("Current registered vehicle: ")
        
        #Vehicle information from the database:  
        for i in range(len(jsonResponse)):

            #vehicle variable that holds the jsonObject:
            vehicle = jsonResponse[i]

            vehicle_id = str(vehicle["_id"])
            vin_number = str(vehicle["vin"])
            vehicle_name = str(vehicle["vehicle_name"])
            vehicle_type = str(vehicle["vehicle_type"])
            vehicle_color = str(vehicle["vehicle_color"])
            status = str(vehicle["is_available"])
            vehicle_location = str(vehicle["vehicle_position"])
            vehicle_status = str(vehicle["vehicle_status"])


            #Dictionary to hold those information:
            vehicle_dictionary = {
                "vehicle_id": vehicle_id,
                "vin_number": vin_number,
                "vehicle_name": vehicle_name,
                "vehicle_type": vehicle_type,
                "vehicle_color": vehicle_color,
                "is_available": status,
                "vehicle_position": vehicle_location,
                "vehicle_status": vehicle_status
            }

            print("vehicle " ,str(i+1), " ",  str(vehicle_dictionary))
        

        #user validation: 
        #Begin the process of removing a vehicle out of the vsim local storge.
        # if(user_input == "Y" or user_input == "y"):
        while True: 
            try: 
                user_input = input("Do you wish to remove a vehicle from the vsim? Y|Yes, N|no ")
                #going through the dictionary and remove each vehicle: 
                user_choice_remove = input("Please enter the name of the vehicles that you want to remove: ")
                for name in range(len(vehicleDictForRemoving)):
                    try:

                        if(user_choice_remove == vehicleDictForRemoving[name]['vehicle_name']):
                            removed_value = vehicle_dictionary.pop(vehicleDictForRemoving[name]['vehicle_name'])
                            print("Vehicle successfully removed from vehicle simulator...")
                    except:
                        print("You did not input the right information, please try again!")
                        continue
            except: 
                print("Something went wrong here! Please enter the name of the vehicles that you want to remove, otherwise, chose N for no: ")
                continue
            
            if(user_input == "N" or user_input == "n"):
                print("")
                break

        #end of program
        else: 
            print("End of task.")

    #HEARTBEAT IMPLEMENTATION: 
    #A vehicle ID will be selected and assigned a "hearbeat" package and then it will send them to the supply side.
    #Each vehicle will send a hearbeat back to the supply server, but each of them will also recieve an order request from the supply server as a response.
    #The supply side will response accordingly to the hearbeat type.
    #The package includes: Vehicle status, location and vehicle id.
    elif choice == 3:
        #  option_3_chosen
        # vID = [vehicleID_2, vehicleID_3]
        # routes = [route_1, route_2]
        # threads = []
        # for i in range(len(vID)):
        #   t = threading.Thread(target=sendingVehicleHeartbeatStatus, args=[vID[i], routes[i]])
        #   t.start()

        #   threads.append(t)

        # [thread.join() for thread in threads]

        #Extracting vehicle id from the server:
        vID_List = vehicleID_Extractor()
        print(vID_List[0])

        
        # for i in range(len(vID_List)):
        #     print(vID_List[i])
        # #Multi-threading implementation: 
        # threads = []
        # for i in range(len(vID_List)):
        #   t = threading.Thread(target=heartBeatSenderAndListener, args=[vID_List[i]])
        #   t.start()

        #   threads.append(t)

        # [thread.join() for thread in threads]


        # #  option_3_chosen()
        t1 = threading.Thread(target=heartBeatSenderAndListener, args=[vID_List[0]])
        t1.start()
        # # # t2 = threading.Thread(target=sendingVehicleHeartbeatStatus, args=[vehicleID_2, route_2])
        # # # t2.start()
        # # # t3 = threading.Thread(target=sendingVehicleHeartbeatStatus, args=[vehicleID_3, route_3])
        # # # t3.start()


        # t1.join()
        # t2.join()
        # t3.join()


       

    #Creating a new vehicle right on the vehicle simulator: 
    #-------------STILL UNDERDEVELOPMENT-------------------
    elif choice == 4: 
        selectVehicle()     

    else:
        print("More functionality construction underway, come back soon!")

#This function will send the heartbeat, listen to the response, analyze it and coordinate vehicles to work on an order based on its status:
def heartBeatSenderAndListener(vehicle_id):
    #For debugging:
    print("Running HeartBeat Listener!")
    print("")

    #API URL to reference the Supply server: 
    API_URL = "https://supply.team12.softwareengineeringii.com/api/heartbeat/requestbeat"


    #Vehicle location from database is:
    vehicleCurrentLocation = vehicleLocation_Extractor(vehicle_id)
    #Heartbeat package to send back to the supply:
    data = {
        "vehicle_id": vehicle_id,
        "vehicle_status": DEFAULT_VEHICLE_STATUS,
        "vehicle_position": vehicleCurrentLocation
    }

    #Sending the request through a POST command:
    request = requests.post(API_URL, json=data)
    #Status of the request:
    print("Sending heartbeat package...")
    print(request.status_code, request.reason)
    response_code = request.status_code    
    #If the post request came back successfully with a response from the database
    #The reponse will be displayed through the terminal.
    if response_code == 200:
        returnStatusPackage = json.loads(request.content)
        supplyConfirmation = str(returnStatusPackage['response'])
        recivedRoute = returnStatusPackage['route']
        print("Supply BE response: " + str(supplyConfirmation))
        print("")
        # print("Supply BE route: " + str(recivedRoute))
        #Check to see if there is a route sent back from the resposnse, if there is pick a vehicle and drive it:
        #There are no route to work on, then the vehicle will remains the same location:
        if not recivedRoute:
            startHeartBeat(vehicle_id, DEFAULT_VEHICLE_STATUS)
        
        else:
            # sendingVehicleHeartbeatStatus(vehicle_id, recivedRoute) #maybe with a vehicle status:
            t = threading.Thread(target=traverse, args=[recivedRoute])
            t.start()
            t.join()

    #Error has occurred:
    #Error handling
    else:
        errorStatus = 'Error Code: ' + str(response_code)
        bytesStr = errorStatus.encode('utf-8')
        print(request.text)
        print(bytesStr)

#Driving a vehicle based on the location sent back from the supply server:
def sendingVehicleHeartbeatStatus(vehicleID, route):
    # vehicleStatus = "OTW"
    # vehicleStatus_Idle = "OK"
    #every vehicle will start out with 'AVAILABLE' status:
    vehicleStatus = 'OTW'
    # vehicleCurrentLocation = vehicleLocationExtractor()
    #URL to the heartbeat API call
    API_URL = "https://supply.team12.softwareengineeringii.com/api/heartbeat/requestbeat"

    #Preparing data package:
    #Heatbeat package:
    for i in range(len(route)):
        #if the vehicle has reached its final stop for an order the vehicle will automatically return to the closest warehouse:
        if i == (len(route)-1):
            vehicleStatus = 'DONE'
            #Getting the route to come back to the warehouse once the 
            backToWarehouseRoute = getRoute(route[i], warehouse_longHorn)
            #The vehicle will return to the warehouse once it finishes an order:
            for i in range(len(backToWarehouseRoute)):
                data = {
                "vehicle_id": vehicleID,
                "vehicle_status": vehicleStatus,
                "vehicle_position": backToWarehouseRoute[i]
            }
                #Converting the dictionary into a JSON object:
                # jsonObject = json.dumps(data)
                # headers = {'content-type': 'application/json'}
                #Sending request through a POST:
                request = requests.post(API_URL, json=data)
                #Status of the request:
                print("Sending heartbeat package...")
                print(request.status_code, request.reason)
                response_code = request.status_code
                #If the post request came back successfully with a response from the database
                #The reponse will be displayed through the terminal.
                if response_code == 200:
                    returnStatusPackage = json.loads(request.content)
                    supplyConfirmation = str(returnStatusPackage['response'])
                    # recivedRoute = str(returnStatusPackage['route'])
                    print("Supply BE response: " + str(supplyConfirmation))
                    print("")
                    # print("Supply BE route: " + str(recivedRoute))

                #Error has occurred:
                #Error handling
                else:
                    errorStatus = 'Error Code: ' + str(response_code)
                    bytesStr = errorStatus.encode('utf-8')
                    print(request.text)
                    print(bytesStr)

                #For testing purposes:
                print("***************Debugging purposes********************")
                print("Vehicle Current Location is: " + str(backToWarehouseRoute[i]))
                print("Vehicle status " + str(vehicleStatus))
                print(backToWarehouseRoute[i])
                print("")
                print("Vehicle being worked with is: " + str(vehicleID))
                time.sleep(5)

        else:
            data = {
            "vehicle_id": vehicleID,
            "vehicle_status": vehicleStatus,
            "vehicle_position": route[i]
        }

            #Converting the dictionary into a JSON object:
            # jsonObject = json.dumps(data)
            # headers = {'content-type': 'application/json'}
            #Sending request through a POST:
            request = requests.post(API_URL, json=data)
            #Status of the request:
            print("Sending heartbeat package...")
            print(request.status_code, request.reason)
            response_code = request.status_code
            #If the post request came back successfully with a response from the database
            #The reponse will be displayed through the terminal.
            if response_code == 200:
                returnStatusPackage = json.loads(request.content)
                supplyConfirmation = str(returnStatusPackage['response'])
                # recivedRoute = str(returnStatusPackage['route'])
                print("Supply BE response: " + str(supplyConfirmation))
                print("")
                # print("Supply BE route: " + str(recivedRoute))

            #Error has occurred:
            #Error handling
            else:
                errorStatus = 'Error Code: ' + str(response_code)
                bytesStr = errorStatus.encode('utf-8')
                print(request.text)
                print(bytesStr)

            #For testing purposes:
            print("***************Debugging purposes********************")
            print("Vehicle Current Location is: " + str(route[i]))
            print("Vehicle status " + str(vehicleStatus))
            print(route[i])
            print("")
            print("Vehicle being worked with is: " + str(vehicleID))
            time.sleep(5)


#Function that will constantly sends the heartbeat to the supply sides:
def startHeartBeat(vehicleID, vehicle_status):
    #Inifite loops to runs the heartbeat forever in the background:
    while vehicle_status != 'OFFLINE':
        heartBeatSenderAndListener(vehicleID)
        time.sleep(15)



#This function will reference the geocoding API from mapbox to find the route between two particular points:
def getRoute(vehilceCurrentLocation, warehouseLocation):
    #Mapbox api key:
    accessToken = "pk.eyJ1Ijoid2lsbGx1b25nOTciLCJhIjoiY2s2bno3OTNvMGRnaTNqcGJzOG9jY2N2ZiJ9.HfvhKBvZreCaO8KFqlYkRw"
    url ='https://api.mapbox.com/directions/v5/mapbox/driving/' + str(vehilceCurrentLocation[0]) + ',' + str(vehilceCurrentLocation[1]) + ';' + str(warehouseLocation[0]) + ',' + str(warehouseLocation[1]) + '?geometries=geojson&access_token=' + accessToken

    #Getting back the response from the API in the form of a json object: 
    response = requests.get(url).json()

    retRoute = response['routes'][0]['geometry']['coordinates']

    return retRoute

#This function will extract vehicle location from the databse:
def vehicleLocation_Extractor(vehicleID):
    #An array to store all vehicle location:
    vehicleLocationFromDatabase = []
    #Making an API call to the supply server to retrieve all vehicles from the supply server to get the vehicle database:
    API_Call = 'https://supply.team12.softwareengineeringii.com/api/backend?vehicle-all=1'
    print("")
    vehicleResponse = requests.get(API_Call).json()
    for i in range(len(vehicleResponse)):
        if vehicleID == vehicleResponse[i]['_id']:
            vehicleLocationFromDatabase = vehicleResponse[i]['vehicle_position']
        
        else:
            break
    
    print("Vehicle: ", str(vehicleID), " position from the server is: ", str(vehicleLocationFromDatabase))
    return vehicleLocationFromDatabase



def traverse (route, time_factor=10, speed_factor=2):
    # route is the response object from Mapbox, contains everything about the route
    # time_factor 1, 1 second will take 1 second
    # time_factor 10, 1 second will take 1/10 seconds

    # speed_factor is to compensate for the slow duration by mapbox
    # speed_factor = 2 will make a car going 22 mph go 44 mph.
    # a car should not be moving 22 mph down south congress that's ridiculous
    
    print ("STARTING ROUTE!")
    
    # Cannot divide by zero so set time_factor back to 1
    # used in time.sleep()
    if (time_factor == 0):
        print ("TIME FACTOR CANNOT BE ZERO, SETTING IT TO 1")
        time_factor = 1
        
    # Cannot divide by zero so set time_factor back to 1
    # used in time.sleep()
    if (speed_factor == 0):
        print ("SPEED FACTOR CANNOT BE ZERO, SETTING IT TO 1")
        speed_factor = 1
        
    # get the route legs
    # legs are essentially stops in our case
    legs = route["routes"][0]["legs"]
    
    # set vehicle position at the start of the route
    vehicle_position = legs[0]["steps"][0]["geometry"]["coordinates"][0]
    
    # get the eta in seconds for the entire route
    vehicle_eta = route["routes"][0]["duration"] / speed_factor
    
    # get the eta in seconds for the next stop
    # initialize with the eta for first stop
    vehicle_next_stop_eta = route["routes"][0]["legs"][0]["duration"] / speed_factor
    
    # get the distance in meters traveled for the entire route
    vehicle_distance = route["routes"][0]["distance"]
    
    # access the route legs
    stop_number = 0
    
    # accessing each leg
    for leg in legs:
        stop_name = leg["summary"]
        print ("Stop", stop_number,":", stop_name)
        
        # get the eta to next stop
        vehicle_next_stop_eta = leg["duration"] / speed_factor
        print ("Next stop ETA:", vehicle_next_stop_eta)
        waypoint_number = 0
        
        # access each step inside the leg
        for step in leg["steps"]:
            waypoint_name = step["name"]
            print ("Waypoint", waypoint_number,":", waypoint_name)
            
            # grab the coordinates to travel through
            coordinates = step["geometry"]["coordinates"]
            
            # time to travel to each coordinate, used for time.sleep()
            step_duration = step["duration"] / speed_factor
            secs_per_coordinate = step_duration / len(coordinates)
            
            # distance to each coordinate
            meters_per_coordinate = step["distance"] / len(coordinates)
            print ("##### STARTING WAYPOINT", waypoint_number, "#####")
            
            # traverse to the position
            for position in coordinates:
                # update vehicle's position
                vehicle_position = position
                
                # update the vehicle's eta for the entire route
                vehicle_eta -= secs_per_coordinate
                
                # update the vehicle's eta for the next stop
                vehicle_next_stop_eta -= secs_per_coordinate
                
                # calculate the mph using meters per second
                if secs_per_coordinate == 0:
                    # avoiding division by zero
                    vehicle_mph = 0
                else:
                    vehicle_mph = mps_to_mph(meters_per_coordinate / secs_per_coordinate)
                
                # output numbers are rounded
                print ("v pos:", vehicle_position, "| dist:", round(meters_per_coordinate, 2), "| secs:", round(secs_per_coordinate, 2), "| MPH: ", round(vehicle_mph), "| next eta: ", round(vehicle_next_stop_eta, 2), "| total eta: ", round(vehicle_eta, 2))
                
                # wait between coordinates
                time.sleep(secs_per_coordinate / time_factor)
                
            print ("!!!!! REACHED WAYPOINT", waypoint_number, "!!!!!")
            waypoint_number += 1
        
        stop_number += 1
        print ("%%%% ARRIVED AT STOP", stop_number, "%%%%")
        print ("")
    print ("************** ARRIVED AT DESTINATION! ***************")

# Convert miles per hour to meters per second
def mph_to_mps(mph):
    return mph * 0.44704

# Convert meters per second to miles per hour
def mps_to_mph(mps):
    return mps * 2.237

def displayVehicle():
    # Requesting to add all vehicle from the database into the local vsim.
    API_Call = 'https://supply.team12.softwareengineeringii.com/api/backend?vehicle-all=1'
    print('\tThe API http string --> ' + API_Call)
    print("")
    jsonResponse = requests.get(API_Call).json()
    # print("Current registered vehicle: ")
    # print(jsonResponse)
    vehicle = json.dumps(jsonResponse)
    vehicle_ID_Array = []
    #Vehicle information from the database: 
    for i in range(len(jsonResponse)):
        #vehicle variable that holds the jsonObject:
        vehicle = jsonResponse[i]
        dummy_transfer = json.dumps(vehicle)
        vehicle_dictionary_2 = json.loads(dummy_transfer)

        vehicle_id = str(vehicle["_id"])
        vin_number = str(vehicle["vin"])
        vehicle_name = str(vehicle["vehicle_name"])
        vehicle_type = str(vehicle["vehicle_type"])
        vehicle_color = str(vehicle["vehicle_color"])
        # status = str(vehicle["is_available"])
        vehicle_location = str(vehicle["vehicle_position"])
        vehicle_status = str(vehicle["vehicle_status"])


        #Dictionary to hold those information:
        vehicle_dictionary = {
            "vehicle_id": vehicle_id,
            "vin_number": vin_number,
            "vehicle_name": vehicle_name,
            "vehicle_type": vehicle_type,
            "vehicle_color": vehicle_color,
            # "is_available": status,
            "vehicle_position": vehicle_location,
            "vehicle_status": vehicle_status
        }

        print("vehicle " ,str(i+1), " ",  str(vehicle_dictionary))
        print("")
    

def vehicleID_Extractor():
    # Requesting to add all vehicle from the database into the local vsim.
    API_Call = 'https://supply.team12.softwareengineeringii.com/api/backend?vehicle-all=1'
    print('\tThe API http string --> ' + API_Call)
    print("")
    jsonResponse = requests.get(API_Call).json()
    vehicleID_array = []
    #extracting the v_id part out of the 
    for i in range(len(jsonResponse)):
        vehicleID_array.append(jsonResponse[i]['_id'])

    return vehicleID_array


def selectVehicle():
    keyLog = []
    # Requesting to add all vehicle from the database into the local vsim.
    API_Call = 'https://supply.team12.softwareengineeringii.com/api/backend?vehicle-all=1'
    print("")
    jsonResponse = requests.get(API_Call).json()
    print("Current registered vehicle: ")
    # print(jsonResponse)
    vehicle = json.dumps(jsonResponse)
    selected_vehicle = [] 
    # print(jsonResponse[0])
    #Vehicle information from the database: 
    for i in range(len(jsonResponse)):
        #
        #vehicle variable that holds the jsonObject:
        vehicle = jsonResponse[i]
        dummy_transfer = json.dumps(vehicle)
        vehicle_dictionary_2 = json.loads(dummy_transfer)

        vehicle_id = str(vehicle["_id"])
        vin_number = str(vehicle["vin"])
        vehicle_name = str(vehicle["vehicle_name"])
        vehicle_type = str(vehicle["vehicle_type"])
        vehicle_color = str(vehicle["vehicle_color"])
        # status = str(vehicle["is_available"])
        vehicle_location = str(vehicle["vehicle_position"])
        vehicle_status = str(vehicle["vehicle_status"])


        #Dictionary to hold those information:
        vehicle_dictionary = {
            "vehicle_id": vehicle_id,
            "vin_number": vin_number,
            "vehicle_name": vehicle_name,
            "vehicle_type": vehicle_type,
            "vehicle_color": vehicle_color,
            # "is_available": status,
            "vehicle_position": vehicle_location,
            "vehicle_status": vehicle_status
        }

        # print("vehicle " ,str(i), " ",  str(vehicle_dictionary))
        # print("")
        
    while True:
        try:
            #User input to select the vehicles based on the index: 
            user_input = int(input("Please enter an index of a vehicle that you want to choose: "))

            
        #Error handling:
        except ValueError:
            print("Something wrong happened here! Please try again...")
            #Return to the start of the loop: 
            continue

        #Extracting the vehicles from the user input:
        else:
            #Logging every input key: 

            keyLog.append(jsonResponse[user_input])
            print("")
            print("The vehicle that you chose: ", str(keyLog), '\n')
            #The user put in a correct format of an integer; break out of the loop and begins the adding vehicles: 
            user_stop_input = input("Do you want to do this again (yes/no)? ")
            if user_stop_input == 'yes':
                continue
            
            else:
                break

    print("The final vehicle array from your selection are:  ", str(keyLog))
        
main()


