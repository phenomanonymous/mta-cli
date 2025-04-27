import pandas as pd
from collections import defaultdict

STOPS_FILE = "gtfs_supplemented/stops.txt"
STATIONS_FILE = "gtfs_supplemented/Stations.csv"

class Stations:
    def __init__(self):
        self.stations_file = STATIONS_FILE
        self.stations_df = pd.read_csv(STATIONS_FILE)
        self.stations = self.get_stations()

    def get_stations(self):
        stops = defaultdict(list)
        stations = []
        for row in self.stations_df.itertuples():
            for route in row.daytime_routes.split():
                stops[route].append(row)
        return stops

class Stops:
  def __init__(self):
    self.stops_file = STOPS_FILE
    self.stops_df = pd.read_csv(STOPS_FILE)
    self.stations = self.get_stations()

  def get_stations(self):
    stops = {}
    # each station is indexed by location
    stations = []
    for row in self.stops_df.itertuples():
      stations.append(str(row.stop_name))   
    stations = list(set(stations))

    count = 0
    for station in stations:
      stops[count] = {'station_id': count, 'name': station, 'stop_ids': []}
      name_found = False
      for row in self.stops_df.itertuples():
        if  str(row.stop_name) == station:
          if name_found == False:
            stops[count]['name'] = row.stop_name
            name_found = True
          stopId = row.stop_id
          if stopId[-1] == "N" or stopId[-1] == "S":
            continue
          else:
            stops[count]['stop_ids'].append(stopId)
      count += 1
    stops2 = []
    for count in stops.keys():
      stops2.append(stops[count])
    return stops2
