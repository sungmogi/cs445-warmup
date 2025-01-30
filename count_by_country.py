import json
from collections import defaultdict

def count_traceroutes_by_country(json_filepath):
    """
    Counts the number of traceroutes that contain each country.
    
    :param json_filepath: Path to the JSON file containing traceroute data.
    :return: Dictionary with country counts.
    """
    country_counts = defaultdict(int)

    # Load traceroute data
    with open(json_filepath, "r") as file:
        traceroutes = json.load(file)

    # Process each traceroute
    for traceroute in traceroutes:
        countries_in_traceroute = set()  # To track unique countries in this traceroute

        for hop in traceroute:
            country = hop.get("country")
            if country:  # Ensure the country field is not None
                countries_in_traceroute.add(country)

        # Count occurrences of each country in this traceroute
        for country in countries_in_traceroute:
            country_counts[country] += 1

    print(json_filepath, dict(country_counts))
    return dict(country_counts)


def aggregate_traceroutes_by_country(json_filepaths):
    """
    Aggregates the number of traceroutes that contain each country from multiple files.

    :param json_filepaths: List of JSON file paths containing traceroute data.
    :return: Aggregated dictionary with country counts.
    """
    aggregated_counts = defaultdict(int)

    for filepath in json_filepaths:
        file_counts = count_traceroutes_by_country(filepath)
        for country, count in file_counts.items():
            aggregated_counts[country] += count

    return dict(aggregated_counts)

if __name__ == "__main__":
    # Example usage
    json_filepaths = [
        # "./data/parsed-traceroutes/NG_61190_output.json",
        # "./data/parsed-traceroutes/NG_62927_output.json",
        "./data/parsed-traceroutes/US_51193_output.json",
        "./data/parsed-traceroutes/US_52849_output.json",
        "./data/parsed-traceroutes/US_65379_output.json",
        "./data/parsed-traceroutes/US_1003387_output.json",
        # "./data/parsed-traceroutes/US_1009823_output.json",
    ]
    result = aggregate_traceroutes_by_country(json_filepaths)
    print(result)