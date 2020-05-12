import time
import math

# REMOVE THIS DURING IMPLEMENTATION
# ONLY FOR TESTING PURPOSES
from mapping_services import Mapping_Services

# MAPBOX API
# https://docs.mapbox.com/api/navigation/#route-object
# route object
    # routes
        # [x]
            # duration
            # distance
            # legs
            # geometry
                # coordinates (for drawing the map route)

# https://docs.mapbox.com/api/navigation/#route-leg-object
# legs object
    # [x]
        # summary
        # steps 
            # [y]
                # summary
                # distance
                # duration
                # geometry
                    # coordinates (for the traversing route)
        # duration
        # distance

# Move through the route divided by a time_factor

def traverse (route, time_factor=1, speed_factor=2):
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

def main():
    
    # Stedwards > Torchy's Tacos
    # https://api.mapbox.com/directions/v5/mapbox/driving/-97.752745,30.228613;-97.751599,30.245429?steps=true&geometries=geojson&access_token=pk.eyJ1Ijoid2lsbGx1b25nOTciLCJhIjoiY2s2bno3OTNvMGRnaTNqcGJzOG9jY2N2ZiJ9.HfvhKBvZreCaO8KFqlYkRw
    # m_services = Mapping_Services(["3001 S Congress Avenue, Austin, TX", "1822 S Congress Avenue, Austin, TX"])

    # Stedwards > Austin Airport > Torchy's Tacos
    # https://api.mapbox.com/directions/v5/mapbox/driving/-97.752745,30.228613;-97.664557,30.20901;-97.751599,30.245429?steps=true&geometries=geojson&access_token=pk.eyJ1Ijoid2lsbGx1b25nOTciLCJhIjoiY2s2bno3OTNvMGRnaTNqcGJzOG9jY2N2ZiJ9.HfvhKBvZreCaO8KFqlYkRw
    # m_services = Mapping_Services(["3001 S Congress Avenue, Austin, TX", "3600 Presidential Blvd, Austin, TX", "1822 S Congress Avenue, Austin, TX"])

    # Stedwards > Torchy's Tacos > Austin Central Library
    # https://api.mapbox.com/directions/v5/mapbox/driving/-97.752745,30.228613;-97.751599,30.245429;-97.751784,30.26613;-97.763281,30.253962?steps=true&geometries=geojson&access_token=pk.eyJ1Ijoid2lsbGx1b25nOTciLCJhIjoiY2s2bno3OTNvMGRnaTNqcGJzOG9jY2N2ZiJ9.HfvhKBvZreCaO8KFqlYkRw
    m_services = Mapping_Services(["3001 S Congress Avenue, Austin, TX", "1822 S Congress Avenue, Austin, TX", "710 W Cesar Chavez St, Austin, TX", "1234 S Lamar Blvd, Austin, TX 78704"])

    # https://api.mapbox.com/directions/v5/mapbox/driving/-97.752745,30.228613;-97.664557,30.20901?steps=true&geometries=geojson&access_token=pk.eyJ1Ijoid2lsbGx1b25nOTciLCJhIjoiY2s2bno3OTNvMGRnaTNqcGJzOG9jY2N2ZiJ9.HfvhKBvZreCaO8KFqlYkRw
    # Stedwards > Austin Airport
    # m_services = Mapping_Services(["3001 S Congress Avenue, Austin, TX", "3600 Presidential Blvd, Austin, TX"])

    # grab the Mapbox response object
    route = m_services.get_directions().directions
    
    # grab the waypoints
    waypoints = route["waypoints"]
    
    # put the stop coordinates in a list
    # you can use this to determine the start point and end point of the route
    stop_coordinates = list()
    for stop in waypoints:
        stop_coordinates.append(stop["location"])
    print ("Stop Coordinates", stop_coordinates)
    
    # move through the route at 10 times faster than realtime
    traverse (route, 10)
    
main();