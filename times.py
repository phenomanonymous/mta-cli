import time

from feed_parser import FeedParser

#from utils import get_updates, get_route_id
from stations import Stops

MAX_TIME_DIFFERENCE = 1800

from pprint import pprint

def get_route_id(entity):
  # get route id to get info on where the train is going
  return entity["tripUpdate"]["trip"]["routeId"]

def get_updates(entity):
  updates = entity["tripUpdate"]["stopTimeUpdate"]
  return updates

class Times:
  def __init__(self, route_id, station_id):
    self.route_id = route_id
    self.station_id = station_id
    self.fp = FeedParser()
    self.feed = self.fp.get_feed(route_id)
    self.train_times = self.get_times()

  def process_update(self, entity, update, times):
    time_difference = self.get_time_difference(update)
    stopId = update['stopId'][:-1]
    if time_difference != None and time_difference > 0 and time_difference < MAX_TIME_DIFFERENCE:
      # add direction to route id 
      # Direction is the last character 'N' or 'S' at the end of the stop Id
      route_id = get_route_id(entity) 
      direction = update['stopId'][-1]
      times.append({'stop_id': stopId, 'route_id': route_id, 'direction': direction, 'time':time_difference})
    return times

  def process_entity(self, entity, times):
    #print(f"entity:{entity}")
    if 'tripUpdate' in entity.keys() and "stopTimeUpdate" in entity['tripUpdate'].keys(): 
      updates = get_updates(entity)
      for update in updates:
        times = self.process_update(entity, update, times)
    return times

  def get_times(self):
    times = []
    for entity in self.feed['entity']:
      times = self.process_entity(entity, times)
    #times = self.process_entity(self.feed['entity'], times)
    #print("times=")
    #pprint(times)
    station_times = self.get_station_times(times)
    return station_times
  
  def get_station_times(self, times):
    station_times = []
    stations = Stops().stations
    for station in stations:
      #print(f"station: {station}")
      stations_dict = {'station_id': station['station_id'], 'trains': []}
      for stopId in station['stop_ids']:
        stop_times = list(filter(lambda time: time['stop_id'] == stopId, times))
        for time in stop_times:
          stations_dict['trains'].append(time)
      stations_dict['trains'] = sorted(stations_dict['trains'], key = lambda i: i['time'])
      station_times.append(stations_dict)
    return station_times

  @staticmethod
  def get_time_difference(update):
    """Return time difference between current time and train arrival/departure time in seconds"""
    if "arrival" in update.keys() and "time" in update["arrival"].keys():
      # time in gtfs feed is in POSIX
      return float(update["arrival"]["time"]) - time.time()
    elif "departure" in update.keys() and "time" in update["departure"].keys():
      return float(update["departure"]["time"]) - time.time()
    else: return None
