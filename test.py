#!env/bin/python

from routes import Routes
from stations import Stations
from times import Times

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
            if station_choice == 0:
                break
            if station_choice > 0 and station_choice <= len(stops):
                station = stops[station_choice-1]
                #print(station)
                #print(station.gtfs_stop_id)
                times = Times(choice, station.gtfs_stop_id).train_times
                #print(station)
                #print(station.gtfs_stop_id)
                #station_route = list(filter(lambda s: s['station_id'] == int(station.gtfs_stop_id), times))
                station_route = []
                for time in times:
                    #print(time)
                    if time['trains'] and station.gtfs_stop_id in time['trains'][0]['stop_id']:
                        for t in time['trains']:
                            station_route.append(f"{t['direction']}-bound {t['route_id']} train arriving in {t['time'] // 60} minutes")
                pprint(station_route)
                break
            else:
                print(f"{station_choice} is not a valid stop ID")
    else:
        print(f"{choice} is not a valid route ID")
