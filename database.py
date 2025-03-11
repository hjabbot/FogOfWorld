import pandas as pd
import geopandas as gpd
import shapely

def reduce_city_data(filename):

    # Read in file as ';' seperated file
    # Convert list of alternate names into python lists rather than long string (same for coords)
    city_df = pd.read_csv(filename, 
                          delimiter=';',
                          converters={'Alternate Names': lambda x: x.split(','),
                                      'Coordinates': lambda x: x.split(',')})

    # Combine 'Name' and 'Alternate Names' into single list per row, remove duplicates
    city_df['Alternate Names'] = city_df.apply(
        lambda row: [row['Name']] if row['Alternate Names'][0] == '' else list(set(row['Alternate Names'] + [row['Name']])), 
        axis=1)

    # Reduce to desired columns
    reduced_city_df = city_df[['ASCII Name', 'Alternate Names', 'Country name EN', 'Population', 'Coordinates']]

    # Rename columns
    reduced_city_df = reduced_city_df.rename(columns={
        'ASCII Name': 'name',
        'Country name EN': 'country',
        'Alternate Names': 'alt_names',
        'Population': 'population',
        'Coordinates': 'geometry'
    })

    # Cast coordinates into shapely points
    reduced_city_df['geometry'] = reduced_city_df.apply(lambda x: shapely.Point(x.geometry[1], x.geometry[0]), axis=1)

    # Convert to GeoDataFrame
    reduced_country_df = gpd.GeoDataFrame(reduced_city_df, crs="EPSG:4326")
    reduced_country_df = reduced_country_df.set_geometry('geometry')

    return reduced_city_df

def reduce_country_data(filename):
    # Read in file as ';' seperated file
    # Convert list of coords into python lists rather than long string
    country_df = pd.read_csv(filename, 
                             delimiter=';',
                             converters={'Geo Point': lambda x: x.split(',')})

    # Combine 'Join Name' and 'Country' into single list per row, remove duplicates
    country_df['Join Name'] = country_df.apply(
                lambda row: list(set([row['Country'], row['Join Name']])), 
                axis=1)

    # Reduce to desired columns
    reduced_country_df = country_df[['Geo Point', 'Geo Shape', 'Country', 'Join Name']]

    # Rename columns
    reduced_country_df = reduced_country_df.rename(columns={
        'Geo Point': 'coordinates',
        'Geo Shape': 'geometry',
        'Country'  : 'name',
        'Join Name': 'alt_names'
    })

    # Cast geojson shape into shapely polygons
    reduced_country_df['geometry'] = shapely.from_geojson(reduced_country_df['geometry'])

    # Convert to GeoDataFrame
    reduced_country_df = gpd.GeoDataFrame(reduced_country_df, crs="EPSG:4326")
    reduced_country_df = reduced_country_df.set_geometry('geometry')

    return reduced_country_df


CITY_DB    = reduce_city_data('data/cities.csv')
COUNTRY_DB = reduce_country_data('data/countries.csv')

