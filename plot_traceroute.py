import json
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import ipaddress

def is_valid_ip(ip):
    """Check if an IP address is public (ignore private/local IPs)."""
    try:
        return not ipaddress.ip_address(ip).is_private
    except ValueError:
        return False

def load_traceroute_data(json_filepath):
    """Loads traceroute data from a JSON file."""
    with open(json_filepath, "r") as file:
        return json.load(file)

def process_traceroute_data(traceroute):
    """
    Processes traceroute data to extract points and paths.
    
    Returns:
    - gdf_points: GeoDataFrame with individual hops as points.
    - gdf_lines: GeoDataFrame with traceroute paths as LineStrings.
    """
    point_data = []  # Stores points for individual hops
    line_data = []   # Stores traceroute paths as line strings

    for path in traceroute:
        hop_points = []
        
        for hop in path:
            ip = hop["hop"]
            lat, lon = hop.get("latitude"), hop.get("longitude")
            
            if lat is not None and lon is not None and is_valid_ip(ip):
                point_data.append({"ip": ip, "lat": lat, "lon": lon})
                hop_points.append(Point(lon, lat))

        # Create a line for the traceroute path if there are multiple hops
        if len(hop_points) > 1:
            line_data.append({"geometry": LineString(hop_points)})

    # Convert to GeoDataFrames
    df_points = pd.DataFrame(point_data)
    gdf_points = gpd.GeoDataFrame(df_points, geometry=gpd.points_from_xy(df_points["lon"], df_points["lat"])) if not df_points.empty else gpd.GeoDataFrame()

    df_lines = pd.DataFrame(line_data)
    gdf_lines = gpd.GeoDataFrame(df_lines, geometry="geometry") if not df_lines.empty else gpd.GeoDataFrame()

    return gdf_points, gdf_lines

def load_world_map(shapefile_path):
    """Loads and returns a GeoDataFrame for the world map."""
    world = gpd.read_file(shapefile_path)
    return world  # Keep the entire world, do not filter only Africa

def load_africa_map(shapefile_path):
    """Loads and returns a GeoDataFrame for the African continent from a local shapefile."""
    world = gpd.read_file(shapefile_path)
    africa = world[world["CONTINENT"] == "Africa"]  # Ensure 'CONTINENT' column is present
    return africa

# def plot_traceroute(gdf_points, gdf_lines, africa_map):
#     """
#     Plots the traceroute data on a map of Sub-Saharan Africa.
    
#     - gdf_points: GeoDataFrame with hops.
#     - gdf_lines: GeoDataFrame with paths.
#     - africa_map: GeoDataFrame containing the Africa map.
#     """
#     fig, ax = plt.subplots(figsize=(10, 10))
#     africa_map.plot(ax=ax, color="lightgrey", edgecolor="black")  # Base map
    
#     if not gdf_lines.empty:
#         gdf_lines.plot(ax=ax, color="blue", linewidth=1, alpha=0.7, label="Traceroute Path")  # Paths
#     if not gdf_points.empty:
#         gdf_points.plot(ax=ax, color="red", markersize=20, alpha=0.8, label="Traceroute Hops")  # Hops

#     # Labels and styling
#     plt.title("Traceroute Visualization on Sub-Saharan Africa Map", fontsize=14)
#     plt.xlabel("Longitude")
#     plt.ylabel("Latitude")
#     plt.legend()
#     plt.grid(True)

#     # Show plot
#     plt.show()

def plot_traceroute(gdf_points, gdf_lines, world_map):
    """
    Plots a single traceroute path on a world map with Africa highlighted.
    
    - gdf_points: GeoDataFrame with hops.
    - gdf_lines: GeoDataFrame with a single traceroute path.
    - world_map: GeoDataFrame containing the world map.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot world map in light grey
    world_map.plot(ax=ax, color="lightgrey", edgecolor="black", alpha=0.5)
    
    # Highlight Africa separately (optional)
    africa = world_map[world_map["CONTINENT"] == "Africa"]
    africa.plot(ax=ax, color="white", edgecolor="black", alpha=0.7) 

    # Plot traceroute paths
    if not gdf_lines.empty:
        gdf_lines.plot(ax=ax, color="blue", linewidth=2, alpha=0.7, label="Traceroute Path")

    # Plot traceroute hops
    if not gdf_points.empty:
        gdf_points.plot(ax=ax, color="red", markersize=30, alpha=0.8, label="Traceroute Hops")

    # Labels and styling
    plt.title("Traceroute Visualization (Global with Africa Highlighted)", fontsize=14)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.show()

def main(json_filepath):
    """Main function to load, process, and plot traceroute data."""
    traceroute = load_traceroute_data(json_filepath)
    gdf_points, gdf_lines = process_traceroute_data(traceroute)
    shapefile_path = "./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"  # Replace with actual path
    africa_map = load_africa_map(shapefile_path)
    world_map = load_world_map(shapefile_path)
    plot_traceroute(gdf_points, gdf_lines, world_map)
    # plot_traceroute(gdf_points, gdf_lines, africa_map)

# Example usage
json_filepath = "data/parsed-traceroutes/US_1009823_output.json"  # Replace with your actual file path
main(json_filepath)
