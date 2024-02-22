import folium
from folium.plugins import HeatMap
import pandas as pd

# Sample DataFrame of latitudes and longitudes
# df = pd.DataFrame({'latitude': [lat1, lat2, ...], 'longitude': [long1, long2, ...]})

import pandas as pd

# Defining the DataFrame with the sample data
df = pd.read_csv('duplicates_removed.csv')


# df = pd.DataFrame(data)


# Calculate the median location to center the map
median_lat = df['latitude'].median()
median_long = df['longitude'].median()

# Create a base map
map_osm = folium.Map(location=[median_lat, median_long], zoom_start=13)

# Add a heatmap layer
HeatMap(data=df[['latitude', 'longitude']], radius=10, blur=15, max_zoom=1).add_to(map_osm)

# Display the map
map_osm.save('heatmap.html')
