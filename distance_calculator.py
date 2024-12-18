from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Average speeds in km/h
WALKING_SPEED = 5          # Walking speed
DRIVING_SPEED = 60         # Average car driving speed in urban areas
MOTORCYCLE_SPEED = 50      # Average motorcycle speed

# Initialize geolocator
geolocator = Nominatim(user_agent="distance_calculator")

def get_location_coordinates(location):
    """
    Get the geographical coordinates (latitude and longitude) of a location.
    """
    try:
        loc = geolocator.geocode(location)
        if loc:
            return (loc.latitude, loc.longitude)
        else:
            print(f"Could not find location: {location}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def calculate_distance_and_time(start_location, destination_location):
    """
    Calculate the distance and estimated travel times between two locations.
    """
    start_coords = get_location_coordinates(start_location)
    dest_coords = get_location_coordinates(destination_location)
    
    if start_coords and dest_coords:
        distance = geodesic(start_coords, dest_coords).kilometers
        
        # Calculate time estimates for each mode
        time_walking = distance / WALKING_SPEED
        time_driving = distance / DRIVING_SPEED
        time_motorcycle = distance / MOTORCYCLE_SPEED

        return {
            "distance_km": distance,
            "time_walking_hr": time_walking,
            "time_driving_hr": time_driving,
            "time_motorcycle_hr": time_motorcycle
        }
    else:
        return None