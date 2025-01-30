import json
from collections import defaultdict

def count_traceroutes_international(json_filepath):
    """
    Counts the number of traceroutes that stayed within the country vs. those that left.

    :param json_filepath: Path to the JSON file containing traceroute data.
    :return: Dictionary with counts of domestic and international traceroutes.
    """
    stayed_within = 0
    left_country = 0

    # Load traceroute data
    with open(json_filepath, "r") as file:
        traceroutes = json.load(file)

    # Process each traceroute
    for traceroute in traceroutes:
        country_set = set()
        
        for hop in traceroute:
            country = hop.get("country")
            if country:
                country_set.add(country)

        # Determine if traceroute stayed within the country
        if len(country_set) <= 1:
            stayed_within += 1
        else:
            left_country += 1
        
        # print(country_set)

    print(json_filepath, stayed_within, left_country)

    return {
        "stayed_within": stayed_within,
        "left_country": left_country
    }


def aggregate_traceroutes_international(json_filepaths):
    """
    Aggregates the number of traceroutes that stayed within a country vs. those that left from multiple files.

    :param json_filepaths: List of JSON file paths containing traceroute data.
    :return: Aggregated dictionary with counts of domestic and international traceroutes.
    """
    aggregated_counts = defaultdict(int)

    for filepath in json_filepaths:
        file_counts = count_traceroutes_international(filepath)
        aggregated_counts["stayed_within"] += file_counts["stayed_within"]
        aggregated_counts["left_country"] += file_counts["left_country"]

    return dict(aggregated_counts)


if __name__ == "__main__":
    # Example usage: List of JSON file paths
    json_filepaths = [
        "./data/parsed-traceroutes/NG_61190_output.json",
        "./data/parsed-traceroutes/NG_62927_output.json",
        # "./data/parsed-traceroutes/US_51193_output.json",
        # "./data/parsed-traceroutes/US_52849_output.json",
        # "./data/parsed-traceroutes/US_65379_output.json",
        # "./data/parsed-traceroutes/US_1003387_output.json",
        # "./data/parsed-traceroutes/US_1009823_output.json",
    ]  # Replace with actual file paths

    result = aggregate_traceroutes_international(json_filepaths)
    print(result)
