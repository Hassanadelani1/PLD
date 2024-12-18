import mysql.connector
from distance_calculator import calculate_distance_and_time
from format import format_text 
class TouristGuideApp:
    def __init__(self):
        # Initialize the database connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="root",  # Replace with your MySQL password
            database="tourist_guide_db"
        )
        self.db_cursor = self.db_connection.cursor()

    def main_menu(self):
        while True:
            print(format_text("\n-----------------------------------------The Tourist Guide App✨------------------------------------------", color="blue", bold=True))
            
            

            print(format_text("\n----------------Welcome to the all-in-one Tourist App 👋. The solution to your problems-------------------",color="blue", bold=True))
            
            print(format_text("\n----------------------------------------------------------------------------------------------------------",color="blue", bold=True))

            print(format_text("\n-------------You can choose from the varieties of functionalities the the app has to offer----------------", color="blue", bold=True))

            print("                                                                 ")
            
            print(format_text("Input 1 to view countries where tourist attractions can be found", color="magenta", bold=True))
            print(format_text("Input 2 to search for an attraction", color="magenta", bold=True))
            print(format_text("Input 3 to calculate the distance of an attraction and cost from your location",color="magenta", bold=True))
            print(format_text("Input 4 to Exit the app", color="magenta", bold=True))

            print(format_text("\n---------------------------------------------------------------------------------------------------------", color="magenta", bold=True))
                
            choice = input(format_text("Select an option (1-4): ", color="magenta", bold=True))
            
            if choice == '1':
                self.display_countries()
            elif choice == '2':
                self.search_attraction()
            elif choice == '3':
                self.calculate_distance_and_cost()
            elif choice == '4':
                print(format_text("Exiting the Tourist Guide. Thank you for using the app. We'll love to see you soon", color="blue", bold=True))
                break
            else:
                print(format_text("Invalid choice. Please try again.", color="blue", bold=True))

    def display_countries(self):
        self.db_cursor.execute("SELECT DISTINCT country FROM attractions")
        countries = self.db_cursor.fetchall()
        if countries:
            print(format_text("\nCountries:", color="cyan", bold=True))
            for idx, country in enumerate(countries, start=1):
                print(format_text(f"{idx}. {country[0]}", color="cyan", bold=True))
            country_choice = input(format_text("Select a country by name or number: ", color="cyan", bold=True))
            
            if country_choice.isdigit() and 1 <= int(country_choice) <= len(countries):
                country_name = countries[int(country_choice) - 1][0]
                self.display_attractions(country_name)
            elif any(country_choice.lower() == country[0].lower() for country in countries):
                self.display_attractions(country_choice)
            else:
                print(format_text("Country not found.", color="", bold=True))
        else:
            print(format_text("No countries available.", color="blue", bold=True))

    def display_attractions(self, country_name):
        query = "SELECT name, description FROM attractions WHERE country = %s"
        self.db_cursor.execute(query, (country_name,))
        attractions = self.db_cursor.fetchall()
        
        if attractions:
            print(format_text(f"\n------Tourist Attractions in {country_name}------", color="blue", bold=True))
            for idx, (name, description) in enumerate(attractions, start=1):
                print(format_text(f"{idx}. {name} - {description}",color="blue", bold=True ))
            attraction_choice = input(format_text("Select an attraction by number or type 'back' to return: ", color="blue", bold=True))

            if attraction_choice.isdigit() and 1 <= int(attraction_choice) <= len(attractions):
                self.display_attraction_details(attractions[int(attraction_choice) - 1][0])
            elif attraction_choice.lower() == 'back':
                return
            else:
                print("Invalid choice.")
        else:
            print(format_text(f"No attractions found for {country_name}.", color="blue", bold=True))

    def display_attraction_details(self, attraction_name):
        # """
        # Fetch and display detailed information about a specific attraction.
        # """
        query = "SELECT name, description, location, best_time, entry_fee, activities FROM attractions WHERE name = %s"
        self.db_cursor.execute(query, (attraction_name,))
        attraction = self.db_cursor.fetchone()
    
        if attraction:
            print(format_text("\n--- Attraction Details ---", color="blue", bold=True))
            print(format_text(f"Name: {attraction[0]}", color="blue", bold=True))          # Corresponds to `name`
            print(format_text(f"Description: {attraction[1]}", color="blue", bold=True))   # Corresponds to `description`
            print(format_text(f"Location: {attraction[2]}", color="blue", bold=True))      # Corresponds to `location`
            print(format_text(f"Best Time to Visit: {attraction[3]}", color="blue", bold=True)) # Corresponds to `best_time`
            print(format_text(f"Entry Fee: {attraction[4]}", color="blue", bold=True))    # Corresponds to `entry_fee`
            print(format_text(f"Activities: {attraction[5]}", color="blue", bold=True) )     # Corresponds to `activities`
        else:
            print(format_text("Attraction not found.", color="blue", bold=True))


    def search_attraction(self):
        search_name = input(format_text("Enter the name of the attraction to search for: ", color="blue", bold=True)).lower()
        query = "SELECT country, name, description FROM attractions WHERE LOWER(name) LIKE %s"
        self.db_cursor.execute(query, (f"%{search_name}%",))
        results = self.db_cursor.fetchall()
        
        if results:
            for country, name, description in results:
                print(format_text(f"\nFound in {country}: {name} - {description}", color="blue", bold=True))
        else:
            print(format_text("No matching attractions found.", color="blue", bold=True));

    def calculate_distance_and_cost(self):
        user_location = input(format_text("Enter your current location: ", color="blue", bold=True))
        destination_name = input(format_text("Enter the name of the attraction you want to visit: ", color="blue", bold=True))
        
        query = "SELECT location FROM attractions WHERE name = %s"
        self.db_cursor.execute(query, (destination_name,))
        destination = self.db_cursor.fetchone()
        
        if destination:
            result = calculate_distance_and_time(user_location, destination[0])
            if result:
                print(format_text(f"Distance to {destination_name}: {result['distance_km']:.2f} km", color="blue", bold=True))
                print(format_text(f"Walking Time: {result['time_walking_hr']:.2f} hours", color="blue", bold=True))
                print(format_text(f"Driving Time: {result['time_driving_hr']:.2f} hours", color="blue", bold=True))
                print(format_text(f"Motorcycle Time: {result['time_motorcycle_hr']:.2f} hours", color="blue", bold=True))
            else:
                print(format_text("Could not calculate distance and time.", color="blue", bold=True))
        else:
            print(format_text("Attraction not found.", color="blue", bold=True))

if __name__ == "__main__":
    app = TouristGuideApp()
    app.main_menu()




