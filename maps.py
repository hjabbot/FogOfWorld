from locations import City, Country, Terminator
from trips import Trip
import plotly.express as px

import geopandas as gpd

class CombinedMap:
    pass

class CountryMap:
    pass

class CityMap:
    pass

class TripMap:
    pass

class TerminatorMap:
    def __init__(self, time):
        self.time = time
        self.terminator = Terminator(self.time)
        self.df = gpd.GeoDataFrame(
                    geometry    = [self.terminator.polygon],
                    index       = [0],
                    data        = {'tod': 'night'}
                )
        self.fig = px.choropleth(
                    self.df,
                    geojson     = self.df.geometry,
                    locations   = self.df.index,
                    color       = 'tod',
                    color_discrete_map = 'rgba(0,0,0,0.5)'
        )
