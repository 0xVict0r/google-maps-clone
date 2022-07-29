from datetime import timedelta, datetime
import geocoder
import traveltimepy as ttpy
import pandas as pd
import pydeck as pdk


def get_route_data(origin, destination, transport_type):

    origin_data = geocoder.arcgis(origin).json
    destination_data = geocoder.arcgis(destination).json
    lat_1, lon_1 = origin_data['lat'], origin_data['lng']
    lat_2, lon_2 = destination_data['lat'], destination_data['lng']

    locations = [
        {"id": "departure", "coords": {"lat": lat_1, "lng": lon_1}},
        {"id": "arrival", "coords": {"lat": lat_2, "lng": lon_2}}
    ]

    departure_search = {
        "id": "main search",
        "departure_location_id": "departure",
        "arrival_location_ids": ["arrival"],
        "transportation": {"type": transport_type},
        "departure_time":  datetime.utcnow().isoformat(),
        "properties": ["travel_time", "distance", "route"]
    }

    out = ttpy.routes(
        locations=locations, departure_searches=departure_search)

    return out


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_coordinates(data):
    parts = data["results"][0]["locations"][0]["properties"][0]["route"]["parts"]
    coords = flatten([part["coords"] for part in parts])
    return coords


def get_duration(data):
    return timedelta(seconds=data["results"][0]
                     ["locations"][0]["properties"][0]["travel_time"])


def get_coords_path(coords):
    lat = [point['lat'] for point in coords]
    long = [point['lng'] for point in coords]

    path = [[long[i], lat[i]] for i in range(len(lat))]

    return path


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def get_plot(path):

    df = pd.DataFrame(columns=["name", "path", "color"])

    color = "#ffe600"

    df.at[0, "name"] = "Trip"
    df.at[0, 'color'] = color
    df["color"] = df["color"].apply(hex_to_rgb)
    df.at[0, "path"] = path

    view_state = pdk.ViewState(
        latitude=(path[0][1]+path[-1][1])/2, longitude=(path[0][0]+path[-1][0])/2, zoom=12)

    layer = pdk.Layer(
        type="PathLayer",
        data=df,
        pickable=True,
        get_color="color",
        width_scale=0.01,
        width_min_pixels=2,
        get_path="path",
        get_width=5,
    )

    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={
                 "text": "{name}"})

    return r
