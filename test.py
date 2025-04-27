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
#pprint(stations)

while True:
    choice = input('Please choose a route ID: ').upper()
    if choice == '0':
        break

    if choice in routes:
        print(f"get stops for {choice}")
        stops = stations[choice]
        count = 1
        for stop in stops:
            print(f"{count}. {stop.stop_name}")
            count += 1
        print()

        while True:
            station_choice = int(input('Please choose a stop ID: '))
            if station_choice > 0 and station_choice <= len(stops):
                station = stops[station_choice]
                print(station)
            else:
                print(f"{station_choice} is not a valid stop ID")
    else:
        print(f"{choice} is not a valid route ID")
