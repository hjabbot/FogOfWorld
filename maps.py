import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd

class CombinedMap:
    def __init__(self, city_lists = [],
                       country_lists = [],
                       trip_lists = [],
                       terminator = None):
        
        city_maps       = [CityMap(city_list)       for city_list    in city_lists]
        country_maps    = [CountryMap(country_list) for country_list in country_lists]
        trip_maps       = [TripMap(trip_list)       for trip_list    in trip_lists]
        terminator_map  = TerminatorMap(terminator)

        all_maps = city_maps + country_maps + trip_maps + [terminator_map]

        self.fig = go.Figure(m.data for m in all_maps)

        self.fig.update_geos(resolution=110,
                             lataxis_showgrid=True, lonaxis_showgrid=True,
                             showocean=True, oceancolor="LightBlue",
                             showlakes=False, lakecolor="LightBlue",
                             projection_type="natural earth",
                             showframe=True
                             )
        
        self.fig.update_layout(height=700, 
                               margin={"r":10,"t":10,"l":10,"b":10},
                               showlegend=False
                               )

        self.fig.update_traces(hoverinfo='none',
                               hovertemplate=None
                               )
        
    def show(self):
        self.fig.show()
class CountryMap:
    def __init__(self, country_list, c='rgba(  0,255,  0, 0.5)'):
        pass

class CityMap:
    def __init__(self, city_list, c='rgba(  0,  0,  0, 1.0)'):
        pass

class TripMap:
    def __init__(self, trip_list, c='rgba(255,  0,  0, 1.0)'):
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
                    color_discrete_map = {'night':'rgba(0,0,0,0.5)',
                                          'day'  :'rgba(0,0,0,0)'}
        )
