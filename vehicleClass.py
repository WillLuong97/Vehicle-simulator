# Supply Side Vehicle class
class Vehicle:

    # Constructor/Initializer
    def __init__(self, vehicle_id, vin, license_plate, service_type, fleet_id, status, location, charge):
        self.vehicle_id = vehicle_id
        self.vin = vin
        self.license_plate = license_plate
        self.service_type = service_type
        self.fleet_id = fleet_id
        self.status = status
        self.location = location
        self.charge = charge
        self.route = []

    def set_route(self, route):
        self.route = route

    def drive(self, time_factor=1, speed_factor=2):
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
        legs = self.route["routes"][0]["legs"]
        
        # set vehicle position at the start of the route
        vehicle_position = self.location
        
        # get the eta in seconds for the entire route
        vehicle_eta = self.route["routes"][0]["duration"] / speed_factor
        
        # get the eta in seconds for the next stop
        # initialize with the eta for first stop
        vehicle_next_stop_eta = legs[0]["duration"] / speed_factor
        
        # get the distance in meters traveled for the entire route
        vehicle_distance = self.route["routes"][0]["distance"]
        
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
                    self.location = vehicle_position = position
                    
                    # update the vehicle's eta for the entire route
                    vehicle_eta -= secs_per_coordinate
                    
                    # update the vehicle's eta for the next stop
                    vehicle_next_stop_eta -= secs_per_coordinate
                    
                    # calculate the mph using meters per second
                    if secs_per_coordinate == 0:
                        # avoiding division by zero
                        vehicle_mph = 0
                    else:
                        vehicle_mph = vutils.mps_to_mph(meters_per_coordinate / secs_per_coordinate)
                    
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
