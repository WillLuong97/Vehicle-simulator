#*********************************************FOR QA REVIEWERS: THE BACKEND SERVER IS UNDERGOING SOME MAJOR CHANGES AT THE MOMENT, PLEASE DON'T RUN THESE CODES AS IT MIGHT INTERFERE WITH THE SERVER MAINTENECE**********************************
#Vehicle simulator 
#FUNCTION: This python file will simulate a vehicle model that would interact with the Supply Back End server through a heartbeat signal relationship.
#Basic Postman documentation for API call to get vehicle information from the database
#https://documenter.getpostman.com/view/10366155/SzS4RT25?version=latest
import json
from enum import Enum
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
heartbeat_rate = 5

class Vehicle:
    status_ok = "AVAILABLE"
    status_otw = "OTW"
    status_done = "DONE"
    status_offline = "OFFLINE"
    accepted_status = [status_ok, status_otw, status_done, status_offline]

    def __init__ (self, vid, vin, vehicle_name, vehicle_type, vehicle_color, vehicle_status, vehicle_position, fleet_id):
        self.vehicle_id = vid
        self.vin = vin
        self.vehicle_name = vehicle_name
        self.vehicle_type = vehicle_type
        self.vehicle_color = vehicle_color
        self.vehicle_status = vehicle_status
        self.vehicle_position = vehicle_position
        self.fleet_id = fleet_id,
        self.route = None
        self.dispatch_id = ""
        self.moving = False

    # getter method for vin
    @property
    def vin(self):
        return self._vin

    # setter method for vin
    @vin.setter
    def vin(self, value):
        self._vin = value

    # getter method for vehicle name
    @property
    def vehicle_name(self):
        return self._vehicle_name

    @vehicle_name.setter
    def vehicle_name(self, value):
        self._vehicle_name = value

    # getter method for vehicle type
    @property
    def vehicle_type(self):
        return self._vehicle_type.name

    # setter method to set vehicle type, checks for enum
    @vehicle_type.setter
    def vehicle_type(self, v_type):
        if (type(v_type) == int):
            #print ("Vehicle Type, received an int")
            self._vehicle_type = Vehicle_Type(v_type)
        elif (type(v_type) == Vehicle_Type):
            #print ("Vehicle Type, received an enum")
            self._vehicle_type = v_type
        elif type(v_type) == str:
            #print ("Vehicle Type, received an str")
            self._vehicle_type = Vehicle_Type[v_type.upper()]
        else:
            print ("VEHICLE CLASS ERROR: Could not set vehicle color! Neither enum, string, nor int")
            raise Exception("Type: " + v_type)

    # getter method for vehicle color
    @property
    def vehicle_color(self):
        return self._vehicle_color

    # setter method to set vehicle type, checks for enum
    @vehicle_color.setter
    def vehicle_color(self, v_color):
        if type(v_color) == str:
            self._vehicle_color = v_color.upper()
        else:
            print ("VEHICLE CLASS ERROR: Could not set vehicle color! Not a string!")
            raise Exception("Color: " + str(v_color))

    # getter method for vehicle position
    @property
    def vehicle_position(self):
        return self._vehicle_position

    # setter method for vehicle position
    @vehicle_position.setter
    def vehicle_position(self, value):
        #print (type(value))
        #print (type(value[0]))
        if type(value) == list and len(value) == 2:
            if type(value[0]) == float:
                self._vehicle_position = value
            else:
                raise Exception("Position needs to be a [Float]: " + str(value))
        else:
            raise Exception("Value not a list or needs to have exactly 2 values: " + str(value))

    # getter method for vehicle position
    @property
    def vehicle_status(self):
        return self._vehicle_status

    # setter method for vehicle position
    @vehicle_status.setter
    def vehicle_status(self, value):
        if type(value) != str:
            raise Exception("ERROR: " + str(value) + " is not a string!")
        elif value.upper() in self.accepted_status:
            self._vehicle_status = value.upper()
        else:
            raise Exception("ERROR: " + str(value) + " is not accepted")
        
    # getter method for route
    @property
    def route(self):
        return self._route
        
    # setter method for route
    @route.setter
    def route(self, route):
        self._route = route
    
    # getter method for fleet id
    @property
    def fleet_id(self):
        return self._fleet_id
        
    # setter method for fleet id
    @fleet_id.setter
    def fleet_id(self, id):
        self._fleet_id = id
        
    # getter method for dispatch id
    @property
    def dispatch_id(self):
        return self._dispatch_id
        
    # setter method for dispatch id
    @dispatch_id.setter
    def dispatch_id(self, id):
        self._dispatch_id = id
        
    # getter method for all values of vehicle
    @property
    def dictionary(self):
        vehicle_dictionary = {
          	"vehicle_id": self.vehicle_id,
            "vin": self.vin,
            "vehicle_name": self.vehicle_name,
            "vehicle_type": self.vehicle_type,
            "vehicle_color": self.vehicle_color,
            "vehicle_position": self.vehicle_position,
            "vehicle_status": self.vehicle_status,
            "fleet_id": self.fleet_id,
            "route": self.route,
            "dispatch_id": self.dispatch_id
        }
        return vehicle_dictionary
    
    def traverse (self, time_factor=10, speed_factor=2):
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
            
        route = self.route
            
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
        
        self.moving = True
        
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
                    self.vehicle_position = position
                    
                    # update the vehicle's eta for the entire route
                    vehicle_eta -= secs_per_coordinate
                    
                    # update the vehicle's eta for the next stop
                    vehicle_next_stop_eta -= secs_per_coordinate
                    
                    # calculate the mph using meters per second
                    if secs_per_coordinate == 0:
                        # avoiding division by zero
                        vehicle_mph = 0
                    else:
                        vehicle_mph = self.mps_to_mph(meters_per_coordinate / secs_per_coordinate)
                    
                    # output numbers are rounded
                    print ("v pos:", self.vehicle_position, "| dist:", round(meters_per_coordinate, 2), "| secs:", round(secs_per_coordinate, 2), "| MPH: ", round(vehicle_mph), "| next eta: ", round(vehicle_next_stop_eta, 2), "| total eta: ", round(vehicle_eta, 2))
                    
                    # wait between coordinates
                    time.sleep(secs_per_coordinate / time_factor)
                    
                print ("!!!!! REACHED WAYPOINT", waypoint_number, "!!!!!")
                waypoint_number += 1
            
            stop_number += 1
            print ("%%%% ARRIVED AT STOP", stop_number, "%%%%")
            print ("")
        print ("************** ARRIVED AT DESTINATION! ***************")
        if self.vehicle_status == "OTW":
            self.vehicle_status = "DONE"
        self.route = None
        self.moving = False

    # Convert miles per hour to meters per second
    def mph_to_mps(self, mph):
        return mph * 0.44704

    # Convert meters per second to miles per hour
    def mps_to_mph(self, mps):
        return mps * 2.237

class Vehicle_Type(Enum):
    BUS = 0
    TRUCK = 1
    VAN = 2
 
def convert_to_vehicle_object (v_dictionary):
    new_vehicle = Vehicle (
        v_dictionary["_id"],
        v_dictionary["vin"], 
        v_dictionary["vehicle_name"], 
        v_dictionary["vehicle_type"], 
        v_dictionary["vehicle_color"], 
        v_dictionary["vehicle_status"],
        v_dictionary["vehicle_position"],
        v_dictionary["fleet_id"])
    return new_vehicle
        
def get_all_vehicles_db ():
    # Requesting to add all vehicle from the database into the local vsim.
    API_Call = 'https://supply.team12.softwareengineeringii.com/api/backend?vehicle-all=1'
    json_response = requests.get(API_Call).content
    all_vehicles = json.loads(json_response)
    return all_vehicles

def movement_thread (vehicle):
    while vehicle.vehicle_status != "OFFLINE":
        if vehicle.route != None and not vehicle.moving:
            print ("MOVEMENT THREAD: ", vehicle.vehicle_status, " MOVING:", vehicle.moving, " ROUTE:", vehicle.route != None)
            vehicle.traverse()
        time.sleep(1)
            
#This function will send the heartbeat, listen to the response, analyze it and coordinate vehicles to work on an order based on its status:
def heartbeat(vehicle):
    #For debugging:
    print("Running HeartBeat for", vehicle.vehicle_name)
    print("")
    vehicle.vehicle_status = "AVAILABLE"
    while vehicle.vehicle_status != "OFFLINE":
        heartbeat_request (vehicle)
        time.sleep(heartbeat_rate)
        
def heartbeat_request (vehicle):
    #API URL to reference the Supply server: 
    API_URL = "https://supply.team12.softwareengineeringii.com/api/heartbeat/requestbeat"
    
    data = {
        "vehicle_id": vehicle.vehicle_id,
        "vehicle_status": vehicle.vehicle_status,
        "vehicle_position": vehicle.vehicle_position
    }
    
    if vehicle.dispatch_id != "":
        data.update ({"dispatch_id": vehicle.dispatch_id})

    #Sending the request through a POST command:
    print("Sending heartbeat package...")
    request = requests.post(API_URL, json=data)
    #Status of the request:
    print(request.status_code, request.reason)
    #The reponse will be displayed through the terminal.
    if request.status_code == 200:
        response_dictionary = json.loads(request.content)
        if response_dictionary["response"] == "DISPATCH":
            print ("DISPATCH")
            vehicle.route = response_dictionary['route']
            vehicle.dispatch_id = response_dictionary['dispatch_id']
            vehicle.vehicle_status = "OTW"

        elif response_dictionary["response"] == "RETURN":
            print ("RETURN")
            vehicle.dispatch_id = None
            vehicle.route = response_dictionary['route']
            vehicle.vehicle_status = "AVAILABLE"

    #Error has occurred:
    #Error handling
    else:
        print(request.status_code, request.text)
        
#Main program that run the vsim
def main():
    #menu with options for vsim control.
    print("Welcome to the Vehicle Simulation Demonstrator")  
    all_vehicles = get_all_vehicles_db()
    all_vehicle_objects = list()
    for vehicle in all_vehicles:
        all_vehicle_objects.append (convert_to_vehicle_object (vehicle))
    vehicle1 = all_vehicle_objects[0]
    t1 = threading.Thread(target=heartbeat, args=[vehicle1], daemon=True)
    tt1 = threading.Thread(target=movement_thread, args=[vehicle1], daemon=True)
    tt1.start()
    t1.start()
    tt1.join()
    # # t2 = threading.Thread(target=sendingVehicleHeartbeatStatus, args=[vehicleID_2, route_2])
    # # t2.start()
    # # t3 = threading.Thread(target=sendingVehicleHeartbeatStatus, args=[vehicleID_3, route_3])
    # # t3.start()
    t1.join()
    
main()


