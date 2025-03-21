from locations import Terminator, Country, City
from trips import Trip
from maps import TerminatorMap, CityMap, TripMap, CountryMap, CombinedMap
from coordinates import Time, Position

from database import CITY_DB, COUNTRY_DB

import datetime

COUNTRY_BY_CITY = {
    'Addis Ababa': 'Ethiopia',
    'Beijing': 'China',
    'Cairo': 'Egypt',
    'Dhaka': 'Bangladesh',
    'Edinburgh': 'United Kingdom',
    'Fes': 'Morocco',
    'Gwangju': 'South Korea',
    'Hanoi': 'Vietnam',
    'Istanbul': 'Turkey',
    'Jakarta': 'Indonesia',
    'Kyiv': 'Ukraine',
    'Lagos': 'Nigeria',
    'Moscow': 'Russia',
    'New York City': 'United States of America',
    'Oslo': 'Norway',
    'Pyongyang': 'North Korea',
    'Quito': 'Ecuador',
    'Rio de Janeiro': 'Brazil',
    'Sydney': 'Australia',
    'Tokyo': 'Japan',
    'Ulan Bator': 'Mongolia',
    'Vancouver': 'Canada',
    'Warsaw': 'Poland',
    'Xochimilco': 'Mexico',
    'Yerevan': 'Armenia',
    'Zurich': 'Switzerland'
}

if __name__ == '__main__':

    current_time        = Time(int(datetime.datetime.now(datetime.UTC).timestamp()))
    current_terminator  = Terminator(current_time)
    terminator_map      = TerminatorMap(current_terminator)

    cities      = [City(city_name=k, country_name=v) for k, v in COUNTRY_BY_CITY.items()]
    countries   = [city.country for city in cities]

    print(list(city.country.name for city in cities))




# fig1 = px.choropleth(country_gdf,   
#                      geojson=country_gdf.geometry,   
#                      locations=country_gdf.index,   
#                      color='visited', 
#                      color_discrete_map={'Harry': 'rgba(255,  0,  0, 0.5)',
#                                          'Steph': 'rgba(  0,  0,255, 0.5)',
#                                          'Both' : 'rgba(  0,255,  0, 0.5)',
#                                          'None' : 'rgba(  0,  0,  0, 1.0)'})


# fig2 = px.choropleth(terminator_df, 
#                      geojson=terminator_df.geometry, 
#                      locations=terminator_df.index, 
#                      color='tod',     
#                      color_discrete_map={'night':'rgba(0,0,0,0.5)'})

# # fig3 = px.line_geo(lat=lats, lon=lons,
# #                    color_discrete_sequence=['rgba(150,0,0,1)'],
# #                    line_dash_sequence=['dot']
# # )

# fig = go.Figure(data = fig1.data + fig2.data)# + fig3.data)

# fig.update_geos(
#     # resolution=50,
#     # showcoastlines=True, coastlinecolor="RebeccaPurple",
#     # showland=True, landcolor="LightGreen",
#     resolution=110,
#     lataxis_showgrid=True, lonaxis_showgrid=True,
#     # showocean=True, oceancolor="LightBlue",
#     # showlakes=False, lakecolor="LightBlue",
#     # showcountries=True, countrycolor="darkgrey",
#     projection_type="natural earth",
#     # projection_type="orthographic",
#     # projection={"type":"natural earth",
#     #             "scale":1},
#     # projection_type="satellite", projection_tilt=-23.5
#     # projection_rotation={'lat':23.5}
#     showframe=True,
# )
# fig.update_layout(height=700, 
#                   margin={"r":10,"t":10,"l":10,"b":10},
#                   showlegend=False,
#                   map_style="dark"
#                   )

# fig.update_traces(hoverinfo='none',hovertemplate=None)


# fig.show()