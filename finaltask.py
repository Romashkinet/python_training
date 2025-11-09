import sqlite3
import sqlite3
import math

import pyodbc

db_name = 'cities.db'

# Function to create database and table if not exist
def create_table(db_name):
    with pyodbc.connect("Driver={SQLite3};Database=" + db_name + "") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS cities (
                            name TEXT PRIMArY KeY,
                            latitude REAL,
                            longitude REAL
                            )
                        """)
        conn.commit()
        cursor.close()



# Function to get city coordinates (either from DB or user input)
def get_city_coordinates(city_name):
    with pyodbc.connect("Driver={SQLite3};Database=" + db_name + "") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM cities WHERE name = ?", (city_name,))
        row = cursor.fetchone()

        if row:
            cursor.close()
            return row[0], row[1]

        else:
            print(f"Coordinates for {city_name} not found.")
            lat = float(input(f"Enter latitude for {city_name}: "))
            lon = float(input(f"Enter longitude for {city_name}: "))

            cursor.execute("INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
                           (city_name, lat, lon))
            conn.commit()
            cursor.close()
            return lat, lon

# Function to calculate distance between two coordinates (Haversine formula)
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    R = 6371.0  # Earth's radius in kilometers

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def main():
    create_table(db_name)

    city1 = input("Enter the first city name: ").strip().capitalize()
    lat1, lon1 = get_city_coordinates(city1)
    city2 = input("Enter the second city name: ").strip().capitalize()
    lat2, lon2 = get_city_coordinates(city2)

    dist = calculate_distance(lat1, lon1, lat2, lon2)
    print(f"The distance between {city1} and {city2} is {dist:.2f} km.")

if __name__ == "__main__":
    main()
