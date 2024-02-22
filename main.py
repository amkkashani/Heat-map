# import folium
# from folium.plugins import HeatMap
# import pandas as pd
#
# # Sample DataFrame of latitudes and longitudes
# # df = pd.DataFrame({'latitude': [lat1, lat2, ...], 'longitude': [long1, long2, ...]})
#
# import pandas as pd
#
# # Defining the DataFrame with the sample data
# df = pd.read_csv('duplicates_removed.csv')
#
#
# # df = pd.DataFrame(data)
#
#
# # Calculate the median location to center the map
# median_lat = df['latitude'].median()
# median_long = df['longitude'].median()
#
# # Create a base map
# map_osm = folium.Map(location=[median_lat, median_long], zoom_start=13)
#
# # Add a heatmap layer
# HeatMap(data=df[['latitude', 'longitude']], radius=10, blur=15, max_zoom=1).add_to(map_osm)
#
# # Display the map
# map_osm.save('heatmap.html')


# try2
# import mgrs
#
# # Create an MGRS object
# m = mgrs.MGRS()
#
# # MGRS coordinate (example: "33TWN0000461383")
# mgrs_coord = "54SVE4915273167"
#
# # Convert MGRS to latitude and longitude
# latlon = m.toLatLon(mgrs_coord.encode('utf-8'))
#
# # Print the result
# print(f"Latitude: {latlon[0]}, Longitude: {latlon[1]}")
#
# local_x = 4915.2801  # Eastward offset in meters
# local_y = 73167.3866  # Northward offset in meters


import mgrs
import math

def apply_displacement(lat_lon, local_x, local_y):
    # Earth's radius in meters
    earth_radius = 6378137

    # Convert latitude and longitude to radians
    lat_rad = math.radians(lat_lon[0])
    lon_rad = math.radians(lat_lon[1])

    # Calculate new latitude in radians
    delta_lat = local_y / earth_radius
    new_lat_rad = lat_rad + delta_lat

    # Calculate new longitude in radians
    # Use the cosine of the average latitude to approximate the change in longitude
    avg_lat = (lat_rad + new_lat_rad) / 2
    delta_lon = local_x / (earth_radius * math.cos(avg_lat))
    new_lon_rad = lon_rad + delta_lon

    # Convert the new latitude and longitude from radians to degrees
    new_lat = math.degrees(new_lat_rad)
    new_lon = math.degrees(new_lon_rad)

    return new_lat, new_lon

# Initialize MGRS object
m = mgrs.MGRS()

# Example MGRS coordinate
mgrs_coord = "54SVE049731"

# Convert MGRS to latitude and longitude
latlon = m.toLatLon(mgrs_coord.encode('utf-8'))

# Displacements in meters
local_y = 4915.2801  # Eastward offset
local_x = 73167.3866  # Northward offset

# Apply displacement
new_lat_lon = apply_displacement(latlon, local_x, local_y)

# Optionally convert back to MGRS (if needed)
new_mgrs_coord = m.toMGRS(new_lat_lon[0], new_lat_lon[1], MGRSPrecision=5)

# Print the results
print(f"Original Latitude: {latlon[0]}, Original Longitude: {latlon[1]}")
print(f"New Latitude: {new_lat_lon[0]}, New Longitude: {new_lat_lon[1]}")
# print(f"New MGRS Coordinate: {new_mgrs_coord.decode('utf-8')}")
