from geopy.distance import geodesic
from geopy.distance import great_circle
from geopy.distance import distance
import math


def haversine(coord1, coord2):
    radius = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))

HomeGPS = (36.847081, 10.141393)
#RemoteSiteGPS = (36.841520, 10.145671)
RemoteSiteGPS = (0, 0)

print("Geodesic:    ", geodesic(HomeGPS, RemoteSiteGPS).km)
print("Great Circle:", great_circle(HomeGPS, RemoteSiteGPS).km)
print("Vincenty:    ", distance(HomeGPS, RemoteSiteGPS).km)
print("Haversine:   ", haversine(HomeGPS, RemoteSiteGPS) / 1000)