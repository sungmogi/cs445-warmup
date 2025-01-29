import requests
import json

def schedule_traceroute(input_json_filepath, probe_ids, user_id, url='http://caitlyn.cs.northwestern.edu/ripeline/schedule'):
    """
    Schedules RIPE Atlas traceroute requests by sending a POST request.
    
    Parameters:
        input_json_filepath (str): Path to the JSON file containing addresses.
        probe_ids (list): List of probe IDs to include in the request.
        user_id (str): Your user ID for the request.
        url (str): The URL for scheduling the traceroute (default is provided).
        
    Returns:
        dict: Response JSON from the server.
    """
    try:
        # Load addresses from the JSON file
        with open(input_json_filepath, 'r') as file:
            addresses = json.load(file)
        
        # Validate addresses format
        if not isinstance(addresses, list):
            raise ValueError("Input JSON must contain a list of addresses.")
        
        # Prepare addresses_and_probes data
        addresses_and_probes = [
            {"address": address, "probes": probe_ids} for address in addresses
        ]
        
        # Prepare request payload
        data = {
            'type': 'traceroute',
            'addresses_and_probes': addresses_and_probes,
            'description': 'Traceroute request scheduled via function',
            'userid': user_id
        }
        
        # Set headers
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Send POST request
        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        # Raise an error for HTTP issues
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()
    
    except FileNotFoundError:
        raise ValueError(f"The file {input_json_filepath} does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in the input file.")
    except requests.RequestException as e:
        raise ValueError(f"Request failed: {e}")


if __name__ == "__main__":
    input_json_filepath = "subsetIP_US.json"
    # probe_ids = [52849, 51193, 55805] # Comcast (7922), AT&T (7018), Verizon
    probe_ids = [16103, 65379, 1009823, 1003387] # Verizon (701), Level 3 Parent (3356), Microsoft (8075), Amazon (16509)
    
    
    # input_json_filepath = "subsetIP_NG.json"
    # probe_ids = [61190, 62927]
    user_id = "sungmogi"

    try:
        response = schedule_traceroute(input_json_filepath, probe_ids, user_id)
        print("Response:", response)
    except ValueError as e:
        print("Error:", e)