import leafmap.kepler as leafmap
import pandas as pd
import os
from shapely.geometry import Point
import random
import datetime
import numpy as np
from itertools import permutations
import requests
import polyline
import geopandas as gpd
from shapely.geometry import LineString

# Function to calculate fuel consumption
empty_truck_consumption = 27  # in L/100KM
full_truck_consumption = 40   # in L/100KM 

def get_distance_duration(departure, destination):
    # Validate input data
    if 'LONGITUDE_departure' not in departure or 'LATITUDE_departure' not in departure:
        raise ValueError("Departure DataFrame must contain 'LONGITUDE_departure' and 'LATITUDE_departure' columns.")
    if 'LONGITUDE_destination' not in destination or 'LATITUDE_destination' not in destination:
        raise ValueError("Destination DataFrame must contain 'LONGITUDE_destination' and 'LATITUDE_destination' columns.")

    # Construct URL for OSRM API request
    url = f"https://router.project-osrm.org/route/v1/driving/{departure['LONGITUDE_departure']},{departure['LATITUDE_departure']};{destination['LONGITUDE_destination']},{destination['LATITUDE_destination']}?overview=full"

    # Send GET request to OSRM API
    r = requests.get(url)
    
    # Check if request was successful
    if r.status_code != 200:
        raise ValueError(f"Error fetching data from OSRM API: {r.text}")

    # Parse JSON response
    data = r.json()

    # Extract distance and duration from response
    distance = data['routes'][0]['distance']
    duration = data['routes'][0]['duration']
    encoded_polyline = data['routes'][0]['geometry']
    return distance, duration , encoded_polyline

def display_time_from_seconds(seconds):
    # Convert seconds to a timedelta object
    time_delta = datetime.timedelta(seconds=seconds)
    
    # Convert the timedelta object to hours, minutes, and seconds
    hours = time_delta.seconds // 3600
    minutes = (time_delta.seconds // 60) % 60
    seconds = time_delta.seconds % 60
    
    # Format and display the time
    return(": {:02d}:{:02d}:{:02d}".format(hours, minutes, seconds))

def calculate_consumption1(order_percentage, dep, dest, actual_load_percentage):
    if dest == 'DEPARTURE':
        return empty_truck_consumption
    if dep == 'DEPARTURE':
        return full_truck_consumption
    
    # Calculate adjusted consumption based on load percentage
    adjusted_load_percentage = actual_load_percentage - order_percentage
    adjusted_consumption = empty_truck_consumption + (full_truck_consumption - empty_truck_consumption) * (actual_load_percentage / 100)
    return adjusted_consumption

def normalize(value, max_value):
    return value / max_value

def TSP_Algorithm(destinations,df):
    departure = [33.1521436, -8.6055754]
    df = pd.merge(df, destinations[['DESTINATION_NUMBER']], on='DESTINATION_NUMBER', how='inner')
    df.loc[len(df)] = {'LATITUDE':departure[0], 'LONGITUDE':departure[1], 'DESTINATION_NAME':'DEPARTURE'}
    # Merge df with itself to create all possible pairs
    merged = pd.merge(df, df, how='cross')
    # Exclude rows where DEPARTURE is the same as DESTINATION
    merged = merged[merged['DESTINATION_NAME_x'] != merged['DESTINATION_NAME_y']]
    # Select relevant columns
    result = merged[['DESTINATION_NAME_x', 'LATITUDE_x', 'LONGITUDE_x', 'DESTINATION_NAME_y', 'LATITUDE_y', 'LONGITUDE_y']]
    # Rename columns
    result.columns = ['DEPARTURE', 'LATITUDE_departure', 'LONGITUDE_departure', 'DESTINATION', 'LATITUDE_destination', 'LONGITUDE_destination']

    # Iterate through each row of the DataFrame
    for index, row in result.iterrows():
        # Create DataFrames for departure and destination
        departures = {'LATITUDE_departure': row['LATITUDE_departure'], 'LONGITUDE_departure': row['LONGITUDE_departure']}
        destination = {'LATITUDE_destination': row['LATITUDE_destination'], 'LONGITUDE_destination': row['LONGITUDE_destination']}
        
        # Calculate distance, duration, and decoded polyline
        distance, duration, encoded_polyline = get_distance_duration(departures, destination)
        
        # Assign distance, duration, and decoded polyline to new columns in the DataFrame
        result.at[index, 'DISTANCE'] = distance
        result.at[index, 'DURATION'] = duration
        result.at[index, 'ENCODED_POLYLINE'] = encoded_polyline


    # Merge filtered_df with destinations DataFrame on 'DESTINATION_NUMBER'
    merged_df = pd.merge(df, destinations[['DESTINATION_NUMBER', 'QUANTITY_ORDERED']], on='DESTINATION_NUMBER', how='inner')

    # Calculate 'Order_quantity_percentage' column
    merged_df['Order_quantity_percentage'] = merged_df['QUANTITY_ORDERED'] * 100 / 33000

    # Create Client_for_delivery DataFrame with 'DESTINATION_NAME' and 'Order_quantity_percentage' columns
    Client_for_delivery = merged_df[['DESTINATION_NAME', 'Order_quantity_percentage']]


    """    # Calculate the length of the filtered destinations
    num_destinations = len(filtered_df)
    # Generate random percentages that sum up to 100
    order_quantity_percentages = [random.randint(1, 100) for _ in range(num_destinations)]
    total_percentage = sum(order_quantity_percentages)
    order_quantity_percentages = [percentage * 100 / total_percentage for percentage in order_quantity_percentages]

    # Create the Client_for_delivery DataFrame
    Client_for_delivery = pd.DataFrame({
        'Order_quantity_percentage': order_quantity_percentages,
        'DESTINATION_NAME': filtered_df['DESTINATION_NAME']
    })"""

    destination_permutations = permutations(Client_for_delivery['DESTINATION_NAME'])

    best_path = None
    best_consumption = float('inf')
    best_score = float('inf')
    best_duration = float('inf')
    best_distance= float('inf')
    max_consumption = 0
    max_duration = 0

    for path in destination_permutations:
        # Reset variables for each permutation
        current_location = 'DEPARTURE'
        visited_destinations = ['DEPARTURE']
        total_consumption = 0
        total_duration=0
        total_score=0
        actual_truck_load_percentage = 100
        for destination in path:
            duration = result.loc[(result['DEPARTURE'] == current_location) & (result['DESTINATION'] == destination), 'DURATION'].iloc[0]
            distance = result.loc[(result['DEPARTURE'] == current_location) & (result['DESTINATION'] == destination), 'DISTANCE'].iloc[0]
            order_percentage = Client_for_delivery.loc[Client_for_delivery['DESTINATION_NAME'] == destination, 'Order_quantity_percentage'].iloc[0]
            consumption = calculate_consumption1(order_percentage, current_location, destination, actual_truck_load_percentage)
            total_consumption += consumption * (distance / 1000) /100 # Convert distance from meters to kilometers
            total_duration += duration
            current_location = destination
            visited_destinations.append(destination)
            actual_truck_load_percentage -= order_percentage
            
        # Return to the departure location
        distance_to_start = result.loc[(result['DEPARTURE'] == current_location) & (result['DESTINATION'] == 'DEPARTURE'), 'DISTANCE'].iloc[0]
        duration_to_start = result.loc[(result['DEPARTURE'] == current_location) & (result['DESTINATION'] == 'DEPARTURE'), 'DURATION'].iloc[0]
        consumption_to_start = empty_truck_consumption * (distance_to_start / 1000) /100
        total_consumption += consumption_to_start
        total_duration += duration_to_start
        # Update max_consumption and max_duration if needed
        if total_consumption > max_consumption:
            max_consumption = total_consumption
        if total_duration > max_duration:
            max_duration = total_duration

    # Generate all possible permutations of destinations
    destination_permutations = permutations(Client_for_delivery['DESTINATION_NAME'])
    # Iterate through each permutation
    i = 1
    for path in destination_permutations:
        # Reset variables for each permutation
        current_location = 'DEPARTURE'
        visited_destinations = ['DEPARTURE']
        total_consumption = 0
        total_duration=0
        total_score=0
        total_distance=0
        actual_truck_load_percentage = 100
        # Calculate total consumption for the permutation
        for destination in path:
            duration = result.loc[(result['DEPARTURE'] == current_location) & (result['DESTINATION'] == destination), 'DURATION'].iloc[0]
            distance = result.loc[(result['DEPARTURE'] == current_location) & (result['DESTINATION'] == destination), 'DISTANCE'].iloc[0]
            order_percentage = Client_for_delivery.loc[Client_for_delivery['DESTINATION_NAME'] == destination, 'Order_quantity_percentage'].iloc[0]
            consumption = calculate_consumption1(order_percentage, current_location, destination, actual_truck_load_percentage)
            total_duration+=duration
            total_consumption += consumption * (distance / 1000) /100 # Convert distance from meters to kilometers
            current_location = destination
            total_distance +=distance
            visited_destinations.append(destination)
            actual_truck_load_percentage -= order_percentage
        
        # Return to the departure location
        distance_to_start = result.loc[(result['DEPARTURE'] == current_location) & (result['DESTINATION'] == 'DEPARTURE'), 'DISTANCE'].iloc[0]
        duration_to_start = result.loc[(result['DEPARTURE'] == current_location) & (result['DESTINATION'] == 'DEPARTURE'), 'DURATION'].iloc[0]
        consumption_to_start = empty_truck_consumption * (distance_to_start / 1000) /100
        total_consumption += consumption_to_start
        total_duration += duration_to_start
        total_distance +=distance_to_start
        # Normalize the values
        normalized_consumption = normalize(total_consumption, max_consumption)
        normalized_duration = normalize(total_duration, max_duration)
        # Calculate the total score
        total_score = normalized_consumption + normalized_duration
        visited_destinations.append('DEPARTURE')

        
        i+=1
        # Update the best path and minimum consumption if this permutation is better
        if total_score < best_score:
            best_consumption = total_consumption
            best_path = visited_destinations
            best_score = total_score
            best_duration = total_duration
            best_distance = total_distance



    # Merge the temporary DataFrame with the original DataFrame df
    sorted_df = df
    # Convert best_path into a dictionary with destination names as keys and indices as values
    best_path_dict = {dest: i for i, dest in enumerate(best_path)}

    # Add a column representing the indices of each destination name based on the best_path order
    sorted_df['best_path_index'] = sorted_df['DESTINATION_NAME'].map(best_path_dict)

    # Sort the DataFrame based on the best_path_index column
    sorted_df = sorted_df.sort_values(by='best_path_index').drop(columns='best_path_index')

    # Initialize lists to store distance and duration
    distances = []
    durations = []

    # Iterate over the best_path list
    for i in range(len(best_path)-1):
        x = best_path[i]
        y = best_path[i+1]
        # Filter the result DataFrame for the specific departure and destination
        segment = result[(result['DEPARTURE'] == x) & (result['DESTINATION'] == y)]
        # Extract distance and duration from the segment and append to respective lists
        distances.append(segment['DISTANCE'].values[0])
        durations.append(segment['DURATION'].values[0])

    # Create DataFrame from the extracted data
    best_path_details = pd.DataFrame({
        'DEPARTURE': best_path[:-1],
        'DESTINATION': best_path[1:],
        'DISTANCE': ["{:.2f}".format(distance/1000) for distance in distances],
        'DURATION': [display_time_from_seconds(duration) for duration in durations]
    })

    return best_path,best_distance/1000,"{:.2f}".format(best_consumption),display_time_from_seconds(best_duration),best_score,result,sorted_df,best_path_details





