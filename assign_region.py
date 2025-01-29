import json

def assign_region(traceroute_data, region_bounds):
    """
    Assigns a region to each hop based on its latitude and longitude.
    
    :param traceroute_data: List of traceroute results, each being a list of hops.
    :param region_bounds: Dictionary mapping region codes to latitude and longitude ranges.
    :return: Modified traceroute data with an added "region" field.
    """
    def get_region(latitude, longitude):
        if latitude is None or longitude is None:
            return None  # No region if coordinates are missing
        
        for region, (lat_range, lon_range) in region_bounds.items():
            lat_min, lat_max = min(lat_range), max(lat_range)
            lon_min, lon_max = min(lon_range), max(lon_range)
            if lat_min <= latitude <= lat_max and lon_min <= longitude <= lon_max:
                return region
        return "Unknown"  # If no region match is found
    
    for traceroute in traceroute_data:
        for hop in traceroute:
            hop["region"] = get_region(hop["latitude"], hop["longitude"])
    
    return traceroute_data

# Example region bounds mapping
region_bounds = {
    "NA": [[15, 83], [-170, -50]],  # North America
    "LAC": [[-55, 32], [-120, -30]],  # Latin America and the Caribbean
    "ECA": [[35, 82], [-25, 180]],  # Europe and Central Asia
    "MENA": [[10, 40], [-20, 60]],  # North Africa and the Middle East
    "SSA": [[-35, 15], [-20, 55]],  # Sub-Saharan Africa
    "SA": [[5, 38], [60, 95]],  # South Asia
    "EAP": [[-50, 55], [95, 180]]  # East Asia and Pacific
}

if __name__ == "__main__":
    # Example usage
    json_filepath = "./data/parsed-traceroutes/NG_61190_output.json"
    
    try:
        with open(json_filepath, 'r') as file:
            traceroute_data = json.load(file)
        
        updated_traceroute_data = assign_region(traceroute_data, region_bounds)
        
        with open(json_filepath, 'w') as file:
            json.dump(updated_traceroute_data, file, indent=4)
        
        print(f"Updated traceroute data saved to {json_filepath}")
    except Exception as e:
        print(f"Error processing file {json_filepath}: {e}")
