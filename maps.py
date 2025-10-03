import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd

class CombinedMap:
    def __init__(self, city_lists = [],
                       country_lists = [],
                       trip_lists = [],
                       terminator = None,
                       colours = []):
        """
        Parent map object that takes traces of child map objects to create a single
        figure with all information displayed

        Args:
            city_lists    (list, optional): 
                List of location.City objects to create maps of
            country_lists (list, optional): 
                List of location.Country objects to create maps of
            trip_lists    (list, optional): 
                List of trip.Trip objects to create maps of
            terminator    (location.Terminator, optional): 
                location.Terminator object to place into map
            colours       (list, optional):
                Colour to plot each MapObject item. 
                Colours are expected to be strings of either standard 
                colours, or 'rgba(r,g,b,a)'
                Length should match max length of country_lists, city_lists, trip_lists
                First colour maps to the first item in *_list sequence
                i.e. First list of countries in 'country_lists' 
                will be coloured the first colour in 'colours', 
                second to second, etc.
        """        
        # Get list of map objects for each type
        city_maps       = [CityMap(city_list)       for city_list    in city_lists]
        country_maps    = [CountryMap(country_list) for country_list in country_lists]
        trip_maps       = [TripMap(trip_list)       for trip_list    in trip_lists]
        terminator_map  = [TerminatorMap(terminator)]

        all_maps        = city_maps + country_maps + trip_maps + terminator_map

        # Combine all fig trace data into single tuple
        # all_figs_data   = tuple((m.fig.data) for m in all_maps)
        all_figs_data   = tuple()
        for m in all_maps:
            all_figs_data += m.fig.data

        # Create new figure from that tuple of traces
        self.fig = go.Figure(data=all_figs_data)

        # Formatting
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

        country_gdf = pd.concat([country.gdf for country in country_list])
        country_gdf = gpd.GeoDataFrame(country_gdf, geometry='geometry')
        country_gdf['colour'] = c
        

        self.fig = px.choropleth(country_gdf,
                                 locations=country_gdf.index,
                                 geojson=country_gdf.geometry,
                                 color='colour',                 # Colour based on column values
                                 color_discrete_map={'name':c})  # Colour to make the map


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
