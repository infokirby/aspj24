from ip2geotools.databases.noncommercial import DbIpCity

def printDetails(ip):
    res = DbIpCity.get(ip, api_key="free")
    print(f"IP Address: {res.ip_address}")
    print(f"Location: {res.city}, {res.region}, {res.country}")
    print(f"Coordinates: (Lat: {res.latitude}, Lng: {res.longitude})")

def geolocate(ip):
    res = DbIpCity.get(ip, api_key="free")
    return res.country