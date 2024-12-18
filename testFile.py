import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="tourist_guide_db"
    )
    print("Connection successful!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
