import json
import requests

ipinfo_token = "94861062afb05e"

def get_geolocation(ip):
    """Fetch geolocation data using ipinfo.io."""
    try:
        data = requests.get(f"https://ipinfo.io/{ip}/json?token={ipinfo_token}").json()
        if "loc" in data and "country" in data:
            lat, lon = map(float, data["loc"].split(","))
            return lat, lon, data["country"]
    except Exception as e:
        print(f"Service error for IP {ip}: {e}")
    
    print(f"Failed to locate IP: {ip}")
    return None, None, None


def process_traceroute(json_filepath):
    """Read the JSON file, update it with geolocation data, and write it back."""
    try:
        # Read the JSON file
        with open(json_filepath, 'r') as file:
            traceroute = json.load(file)
        
        # Update each hop with geolocation data
        for path in traceroute:
            for hop in path:
                ip = hop["hop"]
                if ip != "***" and hop["RTT"] > 0:
                    lat, lon, country = get_geolocation(ip)
                    print(lat, lon, country)
                    hop["latitude"] = lat
                    hop["longitude"] = lon
                    hop["country"] = country  # Now storing country as well
                else:
                    hop["latitude"] = None
                    hop["longitude"] = None
                    hop["country"] = None  # Set country to None if unavailable
        
        # Write the updated data back to the file
        with open(json_filepath, 'w') as file:
            json.dump(traceroute, file, indent=4)
        
        print(f"Traceroute data successfully updated in {json_filepath}")
    
    except Exception as e:
        print(f"Error processing file {json_filepath}: {e}")

if __name__ == "__main__":
    # Example usage
    json_filepath = "./data/parsed-traceroutes/US_1009823_output.json"  # Replace with your file path
    process_traceroute(json_filepath)
