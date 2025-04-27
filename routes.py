import pandas as pd
import numpy as np

ROUTES_FILE = "gtfs_supplemented/routes.txt"

class Routes:

  def __init__(self):
    self.stops_file = ROUTES_FILE
    self.routes_df = pd.read_csv(ROUTES_FILE)
    self.routes = self.get_routes()
  
  def get_routes(self):
    routes = []
    self.routes_df = self.routes_df.fillna("grey")
    for row in self.routes_df.itertuples(): 
        routes.append({'route_id': row.route_id, 'color': row.route_color, 'long_name': row.route_long_name})
    return routes
