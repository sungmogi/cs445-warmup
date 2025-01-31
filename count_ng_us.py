import json
from collections import Counter

def count_countries_before_us(traceroutes):
    country_counts = Counter()
    us_count = 0
    
    for trace in traceroutes:
        countries = [hop["country"] for hop in trace if hop["country"]]
        
        if "US" in countries:
            us_count += 1
            index_us = countries.index("US")
            countries_before_us = set(countries[:index_us])
            
            for country in countries_before_us:
                country_counts[country] += 1
    
    return dict(country_counts), us_count

def main(json_filepath):
    with open(json_filepath, 'r') as file:
        traceroutes = json.load(file)
    
    country_result, us_count = count_countries_before_us(traceroutes)
    print("Countries before US:", country_result)
    print("Count of US instances:", us_count)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <json_filepath>")
        sys.exit(1)
    
    main(sys.argv[1])
