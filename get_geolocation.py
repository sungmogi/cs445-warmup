import json
import requests

def get_geolocation(ip):
    """Fetch geolocation data using multiple services."""
    services = [
        lambda ip: requests.get(f"http://ipwho.is/{ip}").json(),
        lambda ip: requests.get(f"https://ipinfo.io/{ip}/json").json(),
    ]

    for service in services:
        try:
            data = service(ip)
            if "latitude" in data and "longitude" in data:
                return data["latitude"], data["longitude"]
            elif "loc" in data:  # For ipinfo.io
                loc = data["loc"].split(",")
                return float(loc[0]), float(loc[1])
        except Exception as e:
            print(f"Service error for IP {ip}: {e}")
    
    print(f"Failed to locate IP: {ip}")
    return None, None


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
                    lat, lon = get_geolocation(ip)
                    hop["latitude"] = lat
                    hop["longitude"] = lon
                else:
                    hop["latitude"] = None
                    hop["longitude"] = None
        
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
