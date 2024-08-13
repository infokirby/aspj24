from ip2geotools.databases.noncommercial import DbIpCity
import requests

def printDetails(ip):
    res = DbIpCity.get(ip, api_key="free")
    print(f"IP Address: {res.ip_address}")
    print(f"Location: {res.city}, {res.region}, {res.country}")
    print(f"Coordinates: (Lat: {res.latitude}, Lng: {res.longitude})")

def geolocate(ip):
    res = DbIpCity.get(ip, api_key="free")
    print(res.country)
    return res.country

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']

geolocate(get_public_ip())