import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import ipaddress

# Hardcoded JSON data
TRACEROUTE_DATA = [
    {"hop": "154.113.73.198", "RTT": 0.0, "latitude": None, "longitude": None, "country": None},
    {"hop": "10.0.0.1", "RTT": 1.211, "latitude": None, "longitude": None, "country": None},
    {"hop": "154.113.73.197", "RTT": 1.403, "latitude": 6.4541, "longitude": 3.3947, "country": "NG"},
    {"hop": "154.113.144.218", "RTT": 1.295, "latitude": 6.4541, "longitude": 3.3947, "country": "NG"},
    {"hop": "154.113.144.218", "RTT": 1.295, "latitude": 6.4541, "longitude": 3.3947, "country": "NG"},
    {"hop": "***", "RTT": float('-inf'), "latitude": None, "longitude": None, "country": None},
    {"hop": "154.54.61.214", "RTT": 73.98, "latitude": 41.5503, "longitude": -8.42, "country": "PT"},
    {"hop": "154.54.61.101", "RTT": 87.063, "latitude": 43.2627, "longitude": -2.9253, "country": "ES"},
    {"hop": "154.54.85.241", "RTT": 157.459, "latitude": 39.0437, "longitude": -77.4875, "country": "US"},
    {"hop": "154.54.7.158", "RTT": 173.841, "latitude": 33.749, "longitude": -84.388, "country": "US"},
    {"hop": "154.54.28.70", "RTT": 187.343, "latitude": 29.9324, "longitude": -95.3802, "country": "US"},
    {"hop": "154.54.0.54", "RTT": 203.352, "latitude": 31.7587, "longitude": -106.4869, "country": "US"},
    {"hop": "154.54.166.58", "RTT": 211.721, "latitude": 33.4484, "longitude": -112.074, "country": "US"},
    {"hop": "154.54.28.142", "RTT": 212.318, "latitude": 33.4484, "longitude": -112.074, "country": "US"},
    {"hop": "38.88.238.226", "RTT": 229.43, "latitude": 33.4484, "longitude": -112.074, "country": "US"},
    {"hop": "100.65.240.50", "RTT": 252.483, "latitude": None, "longitude": None, "country": None},
    {"hop": "100.65.248.134", "RTT": 239.903, "latitude": None, "longitude": None, "country": None},
    {"hop": "***", "RTT": float('-inf'), "latitude": None, "longitude": None, "country": None},
    {"hop": "***", "RTT": float('-inf'), "latitude": None, "longitude": None, "country": None},
    {"hop": "***", "RTT": float('-inf'), "latitude": None, "longitude": None, "country": None},
    {"hop": "***", "RTT": float('-inf'), "latitude": None, "longitude": None, "country": None},
    {"hop": "***", "RTT": float('-inf'), "latitude": None, "longitude": None, "country": None},
    {"hop": "***", "RTT": float('-inf'), "latitude": None, "longitude": None, "country": None}
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
    plt.title("Traceroute Visualization", fontsize=14)
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
