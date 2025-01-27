import json
import random


def select_random_subset(country_code, num_domains):
    """
    Selects a random subset of domains from a JSON file for a given country code
    and saves it to a new JSON file.

    Args:
        country_code (str): The country code used to identify the JSON file.
        num_domains (int): The number of domains to select.

    Returns:
        None
    """
    # Construct the JSON file name
    input_filename = f"govtResources_{country_code}.json"
    output_filename = f"randomSubset_{country_code}.json"
    
    try:
        # Load the JSON file
        with open(input_filename, "r") as file:
            domains = json.load(file)
        
        # Check if the number of domains is greater than the list size
        if num_domains > len(domains):
            print(f"Warning: Requested {num_domains} domains, but only {len(domains)} available.")
            num_domains = len(domains)
        
        # Randomly select the specified number of domains
        random_subset = random.sample(domains, num_domains)
        
        # Save the selected subset to a new JSON file
        with open(output_filename, "w") as output_file:
            json.dump(random_subset, output_file, indent=4)
        
        print(f"Random subset saved to {output_filename}")
    
    except FileNotFoundError:
        print(f"Error: The file {input_filename} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {input_filename} could not be decoded as JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    select_random_subset("US", 30)