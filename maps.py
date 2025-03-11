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
    def __init__(self, terminator):
        """
        Creates figure of terminator boundary, shows night region of earth as shaded

        Args:
            terminator (locations.Terminator): Terminator object defined in locations.py
        """
        self.terminator = terminator

        # Terminator marks binary field
        # Set data as 'tod' (time of day), with 'night' as the value to shade
        self.df = gpd.GeoDataFrame(
                    geometry    = [self.terminator.polygon],
                    index       = [0],
                    data        = {'tod': 'night'}
                )
        
        # Draw shade in the 'night' area
        self.fig = px.choropleth(
                    self.df,
                    geojson     = self.df.geometry,
                    locations   = self.df.index,
                    color       = 'tod',
                    color_discrete_map = 'rgba(0,0,0,0.5)'
        )
