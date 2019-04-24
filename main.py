import folium
import json
import overpy

from constants import *

with open('route.geojson', encoding='utf-8') as geojson:
    data = json.load(geojson)
    geometry = data.get('geometry')

coordinates = []
for lat, lon in geometry.get('coordinates'):
    coordinates.append((lon, lat))

middle_idx = len(coordinates) // 2
center = coordinates[middle_idx]

my_map = folium.Map(location=center, zoom_start=6)
folium.PolyLine(coordinates).add_to(my_map)

api = overpy.Overpass()

for latitude, longitude in coordinates[::NTH_POINT]:
    result = api.query(
        QUERY_TEMPLATE.format(
            tag=TAG, radius=RADIUS, lat=lat, lon=lon
        )
    )

for node in result.nodes:
    folium.map.Marker([node.lat, node.lon], popup=node.tags.get('brand', TAG)).add_to(my_map)

my_map.save('map.html')