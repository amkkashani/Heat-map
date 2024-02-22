# import mgrs
# from pyproj import Proj, transform
#
# def apply_local_offsets(mgrs_code, local_x, local_y):
#     # Initialize MGRS converter
#     m = mgrs.MGRS()
#
#     # Convert MGRS to latitude and longitude
#     latlon = m.toLatLon(mgrs_code.encode('utf-8'))
#
#     # Initialize WGS84 projection (used by GPS)
#     wgs84 = Proj(init='epsg:4326')
#
#     # Determine UTM zone and hemisphere from latitude
#     utm_zone = int((latlon[1] + 180) / 6) + 1
#     hemisphere = 'north' if latlon[0] >= 0 else 'south'
#
#     # Initialize UTM projection
#     utm = Proj(proj='utm', zone=utm_zone, ellps='WGS84', south=hemisphere=='south')
#
#     # Project latlon to UTM
#     x, y = transform(wgs84, utm, latlon[1], latlon[0])
#
#     # Apply local offsets
#     x_adjusted = x + local_x
#     y_adjusted = y + local_y
#
#     # Convert adjusted UTM back to lat/lon
#     lon_adjusted, lat_adjusted = transform(utm, wgs84, x_adjusted, y_adjusted)
#
#     return lat_adjusted, lon_adjusted
#
# # Example MGRS data and local offsets
# mgrs_code = "54SVE049731"
# local_x = 4915.2801 # Eastward offset in meters
# local_y = 73167.3866  # Northward offset in meters
#
# # Apply offsets and get adjusted coordinates
# adjusted_lat, adjusted_lon = apply_local_offsets(mgrs_code, local_x, local_y)
#
# print(f"Adjusted Latitude: {adjusted_lat}, Adjusted Longitude: {adjusted_lon}")


import mgrs
from pyproj import Transformer


def mgrs_to_latlon_with_offset(mgrs_code, local_x, local_y):
    # Initialize MGRS converter
    m_converter = mgrs.MGRS()

    # Convert MGRS to latitude and longitude
    latlon = m_converter.toLatLon(mgrs_code.encode('utf-8'))

    # Extract initial latitude and longitude
    initial_lat, initial_lon = latlon

    # Find UTM zone and hemisphere from the MGRS code
    utm_zone = mgrs_code[:3]
    is_southern = 'S' in mgrs_code

    # Define transformer from UTM to WGS84 (and vice versa)
    # This automatically considers the hemisphere based on latitude
    transformer_to_utm = Transformer.from_crs(f"EPSG:4326", f"EPSG:326{utm_zone[:2]}", always_xy=True)
    transformer_to_wgs = Transformer.from_crs(f"EPSG:326{utm_zone[:2]}", "EPSG:4326", always_xy=True)

    if is_southern:
        transformer_to_utm = Transformer.from_crs(f"EPSG:4326", f"EPSG:327{utm_zone[:2]}", always_xy=True)
        transformer_to_wgs = Transformer.from_crs(f"EPSG:327{utm_zone[:2]}", "EPSG:4326", always_xy=True)

    # Convert initial latlon to UTM
    x, y = transformer_to_utm.transform(initial_lon, initial_lat)

    # Apply offsets
    x_adjusted = x + local_x
    y_adjusted = y + local_y

    # Convert back to WGS84
    lon_adjusted, lat_adjusted = transformer_to_wgs.transform(x_adjusted, y_adjusted)

    return lat_adjusted, lon_adjusted


# MGRS code and local offsets
mgrs_code = "54SVE049731"
local_x = 15.2801  # Eastward offset in meters
local_y = 67.3866  # Northward offset in meters

# Adjusted latitude and longitude after applying offsets
adjusted_lat, adjusted_lon = mgrs_to_latlon_with_offset(mgrs_code, local_x, local_y)

print(f"Adjusted Latitude: {adjusted_lat}, Adjusted Longitude: {adjusted_lon}")

