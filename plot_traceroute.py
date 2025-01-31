import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import ipaddress

# Hardcoded JSON data
TRACEROUTE_DATA = [
    {"hop": "196.216.149.17", "RTT": 0.0, "latitude": None, "longitude": None, "country": None},
    {"hop": "192.168.20.1", "RTT": 1.511, "latitude": None, "longitude": None, "country": None},
    {"hop": "197.157.66.160", "RTT": 1.496, "latitude": 6.4541, "longitude": 3.3947, "country": "NG"},
    {"hop": "41.78.188.5", "RTT": 3.51, "latitude": 6.4541, "longitude": 3.3947, "country": "NG"},
    {"hop": "41.78.188.147", "RTT": 104.588, "latitude": 51.5085, "longitude": -0.1257, "country": "GB"},
    {"hop": "212.119.4.176", "RTT": 107.33, "latitude": 51.5085, "longitude": -0.1257, "country": "GB"},
    {"hop": "129.250.6.112", "RTT": 104.946, "latitude": 51.5085, "longitude": -0.1257, "country": "GB"},
    {"hop": "129.250.2.111", "RTT": 181.54, "latitude": 39.0437, "longitude": -77.4875, "country": "US"},
    {"hop": "129.250.3.189", "RTT": 243.438, "latitude": 34.0522, "longitude": -118.2437, "country": "US"},
    {"hop": "129.250.3.245", "RTT": 238.899, "latitude": 34.0522, "longitude": -118.2437, "country": "US"},
    {"hop": "168.143.228.173", "RTT": 240.172, "latitude": 34.0522, "longitude": -118.2437, "country": "US"},
    {"hop": "162.215.195.128", "RTT": 244.291, "latitude": 34.0522, "longitude": -118.2437, "country": "US"},
    {"hop": "162.215.195.141", "RTT": 242.689, "latitude": 40.2338, "longitude": -111.6585, "country": "US"},
    {"hop": "69.195.64.103", "RTT": 242.316, "latitude": 40.2338, "longitude": -111.6585, "country": "US"},
    {"hop": "162.144.240.43", "RTT": 242.331, "latitude": 40.2338, "longitude": -111.6585, "country": "US"},
    {"hop": "142.4.18.72", "RTT": 242.21, "latitude": 40.3544, "longitude": -110.7101, "country": "US"}
]

def is_valid_ip(ip):
    """Check if an IP address is public (ignore private/local IPs)."""
    try:
        return not ipaddress.ip_address(ip).is_private
    except ValueError:
        return False

def process_traceroute_data(traceroute):
    """
    Processes traceroute data to extract points and paths.
    Returns:
    - gdf_points: GeoDataFrame with individual hops as points.
    - gdf_lines: GeoDataFrame with traceroute paths as LineStrings.
    """
    point_data = []
    hop_points = []
    
    for hop in traceroute:
        ip = hop["hop"]
        lat, lon = hop.get("latitude"), hop.get("longitude")
        
        if lat is not None and lon is not None and is_valid_ip(ip):
            point_data.append({"ip": ip, "lat": lat, "lon": lon})
            hop_points.append(Point(lon, lat))

    # Create a line for the traceroute path if there are multiple hops
    gdf_lines = gpd.GeoDataFrame(
        [{"geometry": LineString(hop_points)}], geometry="geometry"
    ) if len(hop_points) > 1 else gpd.GeoDataFrame()

    df_points = pd.DataFrame(point_data)
    gdf_points = gpd.GeoDataFrame(df_points, geometry=gpd.points_from_xy(df_points["lon"], df_points["lat"])) if not df_points.empty else gpd.GeoDataFrame()
    
    return gdf_points, gdf_lines

def plot_traceroute(gdf_points, gdf_lines, world_map):
    """
    Plots a single traceroute path on a world map.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    world_map.plot(ax=ax, color="lightgrey", edgecolor="black", alpha=0.5)
    if not gdf_lines.empty:
        gdf_lines.plot(ax=ax, color="blue", linewidth=2, alpha=0.7, label="Traceroute Path")
    if not gdf_points.empty:
        gdf_points.plot(ax=ax, color="red", markersize=30, alpha=0.8, label="Traceroute Hops")
    # plt.title("Traceroute Visualization", fontsize=14)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    gdf_points, gdf_lines = process_traceroute_data(TRACEROUTE_DATA)
    shapefile_path = "./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
    world_map = gpd.read_file(shapefile_path)
    plot_traceroute(gdf_points, gdf_lines, world_map)

if __name__ == "__main__":
    main()
