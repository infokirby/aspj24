import socket, requests
import numpy as np
from ip2geotools.databases.noncommercial import DbIpCity
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()
Faker.seed(42)

# Define parameters
num_records = 100  # Number of records to generate
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 7, 24)

# Function to generate weighted random timestamps
def generate_weighted_timestamp():
    while True:
        # Generate a random date and time
        random_date = fake.date_time_between(start_date=start_date, end_date=end_date)
        # Heavily weight the time towards 9 AM to 5 PM
        if 9 <= random_date.hour < 17 and random_date.weekday() < 5:
            return random_date

# Function to generate IP addresses mostly located in Singapore
def generate_singapore_ip():
    singapore_ip_blocks = [
        "103.1.104.0/22", "103.3.56.0/22", "103.4.92.0/22", "103.4.224.0/22", 
        "103.5.24.0/22", "103.5.56.0/22", "103.6.4.0/22", "103.6.100.0/22"
    ]
    block = random.choice(singapore_ip_blocks)
    base_ip = block.split('/')[0]
    parts = base_ip.split('.')
    ip = '.'.join(parts[:2]) + '.' + str(random.randint(0, 255)) + '.' + str(random.randint(0, 255))
    return ip




def printDetails(ip):
    res = DbIpCity.get(ip, api_key="free")
    print(f"IP Address: {res.ip_address}")
    print(f"Location: {res.city}, {res.region}, {res.country}")
    print(f"Coordinates: (Lat: {res.latitude}, Lng: {res.longitude})")

def ipCountry(ip):
    res = DbIpCity.get(ip, api_key="free")
    country = res.country
    return country

# Generate synthetic data
data = []
for _ in range(num_records):
    record = {
        'timestamp': generate_weighted_timestamp(),
        'location': ipCountry(generate_singapore_ip()),
        'success': random.choice([True, False])
    }
    data.append(record)

# Create a DataFrame
df = pd.DataFrame(data)

# Display the first few rows of the DataFrame
print(df.head())