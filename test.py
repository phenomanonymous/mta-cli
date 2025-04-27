#!env/bin/python

from routes import Routes
from stations import Stations

from pprint import pprint

r = Routes().routes
routes = {}
for route in r:
    routes[route['route_id']] = route
for route in routes:
    print(f"{route}: {routes[route]['long_name']}")
print()

stations = Stations().stations
pprint(stations)

while True:
    choice = input('Please choose a route ID: ').upper()
    if choice == '0':
        break

    if choice in routes:
        print(f"get stops for {choice}")
    else:
        print(f"{choice} is not a valid route ID")
