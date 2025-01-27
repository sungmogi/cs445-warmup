import json
import random
from urllib.parse import urlparse
import csv


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


def extract_domains_from_file(input_file, output_file):
    """
    Extracts domains from a JSON file containing a list of URLs and writes them to another JSON file.
    
    Parameters:
        input_file (str): The path to the input JSON file containing URLs.
        output_file (str): The path to the output JSON file for the extracted domains.
    """
    try:
        # Read the input JSON file
        with open(input_file, 'r') as file:
            url_list = json.load(file)
        
        if not isinstance(url_list, list):
            raise ValueError("The input JSON file must contain a list of URLs.")
        
        # Extract domains
        domains = []
        for url in url_list:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            if domain.startswith('www.'):
                domain = domain[4:]  # Remove 'www.' prefix
            domains.append(domain)
        
        # Write the domains to the output JSON file
        with open(output_file, 'w') as file:
            json.dump(domains, file, indent=4)
        
        print(f"Domains successfully written to {output_file}")
    
    except FileNotFoundError:
        raise ValueError(f"The file {input_file} does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in the input file.")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")


def map_domains_to_ips(json_input_file, csv_input_file, output_file):
    """
    Maps domains from a JSON file to IP addresses using a CSV file and outputs the results to a JSON file.
    
    Parameters:
        json_input_file (str): The path to the JSON file containing the list of domains.
        csv_input_file (str): The path to the CSV file containing domain-to-IP mappings.
        output_file (str): The path to the output JSON file for the IP addresses.
    """
    try:
        # Read the JSON file
        with open(json_input_file, 'r') as file:
            domains = json.load(file)
        
        if not isinstance(domains, list):
            raise ValueError("The input JSON file must contain a list of domains.")
        
        # Convert domains to lowercase for case-insensitive comparison
        domains = [domain.lower() for domain in domains]
        
        # Read the CSV file and create a domain-to-IP mapping
        domain_ip_map = {}
        with open(csv_input_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                # Extract domain and IP from the CSV (assuming domain is in the 2nd column and IP in the 3rd column)
                csv_domain = row[1].strip().lower()
                ip_address = row[2].strip()
                domain_ip_map[csv_domain] = ip_address
        
        # Map the domains to IPs
        ip_addresses = [domain_ip_map.get(domain, None) for domain in domains]
        
        # Write the results to the output JSON file
        with open(output_file, 'w') as file:
            json.dump(ip_addresses, file, indent=4)
        
        print(f"IP addresses successfully written to {output_file}")
    
    except FileNotFoundError as e:
        raise ValueError(f"File not found: {e}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in the input file.")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")


if __name__ == "__main__":
    # select_random_subset("NG", 50)
    # extract_domains_from_file("randomSubset_NG.json", "subsetDomain_NG.json")
    map_domains_to_ips("subsetDomain_NG.json", "vantage_domain_ip_server_map.csv", "subsetIP_NG.json")