import pandas as pd
import geopandas as gpd
import shapely
import json

def reduce_city_data(filename="data/cities.csv", 
                     country_amendments_filename="data/nan_country_by_city.json"):
    """
    Reduces raw csv with all city data down to the few columns we care about.
    Adds in amendments to the countries for cities with NaN country values.
    Amendments file is manually created and could be prone to errors. 

    Args:
        filename (str, optional): 
            Filename of raw dataset of cities, their locations, population, and country. 
            Defaults to "data/cities.csv".
        country_amendments_filename (str, optional): 
            Manually created amendments to country column of city database.  
            Defaults to "data/nan_country_by_city.json".

    Returns:
        geopandas.GeoDataFrame: 
            Dataframe containing every city (with a large enough population) on Earth
            Dataframe contains these columns:
                'name'      (str)           : City name
                'country'   (str)           : Country name
                'alt_names' (list)          : List of alternate names that city is called (includes value from 'name' column)
                'population'(int)           : Population of city 
                'geometry'  (shapely.Point) : Location of city
    """
    # Read in file as ';' seperated file
    # Convert list of alternate names into python lists rather than long string (same for coords)
    city_df = pd.read_csv(filename, 
                          delimiter=';',
                          converters={'Alternate Names': lambda x: x.split(','),
                                      'Coordinates': lambda x: x.split(',')})
    
    # Read in file containing mapping between names in city database to names in country database
    # NOTE: This file only includes cities that have 'NaN' as their country in the original database
    #       This file exists to fill in those gaps. It pulls in the closest country from the country database and uses that
    #       Only exceptions are small islands that mapped to Guam, which have been manually changed to Micronesia
    with open(country_amendments_filename, 'r') as fp:
        extra_countries = json.load(fp)

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
    # Add list of alt_names to df so that can reference database with more options
    reduced_city_df['country'] = reduced_city_df.apply(lambda row: extra_countries[row['name']] if not isinstance(row['country'], str) else row['country'], axis=1)

    # Convert to GeoDataFrame
    reduced_country_df = gpd.GeoDataFrame(reduced_city_df, crs="EPSG:4326")
    reduced_country_df = reduced_country_df.set_geometry('geometry')

    return reduced_city_df


def reduce_country_data(filename="data/countries.csv", 
                        alt_name_amendments_filename="data/country_alt_names.json"):
    """
    Reduces raw csv with all country data down to the few columns we care about.
    Adds in amendments to expand the country's alternative names list for easier referencing later.
    Amendments file is manually created and could be prone to errors. 

    Args:
        filename (str, optional): 
            Filename of raw dataset of countries, their shapes, and their alternative names. 
            Defaults to "data/cities.csv".
        alt_name_amendments_filename (str, optional): 
            Manually created amendments to alt_names column of country database.  
            Defaults to "data/country_alt_names.json".

    Returns:
        geopandas.GeoDataFrame: 
            Dataframe containing every city (with a large enough population) on Earth
            Dataframe contains these columns:
                'name'      (str)             : Country name
                'alt_names' (list)            : List of alternate names that country is called (includes value from 'name' column)
                'geometry'  (shapely.Polygon) : Shape of country
                'coordinates (shapely.Point)  : Rough location of centre of country
    """
    # Read in file as ';' seperated file
    # Convert list of coords into python lists rather than long string
    country_df = pd.read_csv(filename, 
                             delimiter=';',
                             converters={'Geo Point': lambda x: x.split(',')})

    # Read in file containing mapping between names in country database to alternative names (e.g. names in city database)
    # NOTE: Some poor mapping exist, e.g. South Sudan and Sudan lumped together, Timor Leste lumped in with Indonesia
    #       This is a limitation of the country database file. Needs to be updated with new shapefile geometries for each country
    with open(alt_name_amendments_filename, 'r') as fp:
        alt_names = json.load(fp)

    # Reduce to desired columns
    reduced_country_df = country_df[['Geo Point', 'Geo Shape', 'Country']]

    # Rename columns
    reduced_country_df = reduced_country_df.rename(columns={
        'Geo Point': 'coordinates',
        'Geo Shape': 'geometry',
        'Country'  : 'name'
    })
    # Add list of alt_names to df so that can reference database with more options
    reduced_country_df['alt_names'] = reduced_country_df.name.apply(lambda x: alt_names[x])

    # Cast geojson shape into shapely polygons
    reduced_country_df['geometry'] = shapely.from_geojson(reduced_country_df['geometry'])

    # Convert to GeoDataFrame
    reduced_country_df = gpd.GeoDataFrame(reduced_country_df, crs="EPSG:4326")
    reduced_country_df = reduced_country_df.set_geometry('geometry')

    return reduced_country_df


def find_city_in_country(city_name, country_name):
    """
    Extracts out a single city based off a city name and country name
    Need both as there are duplicate city names

    Args:
        city_name    (str): Name of city
        country_name (str): Name of country the city belongs to

    Returns:
        tuple(pd.Series, pd.Series): row in CITY_DB that contains the correct city,
                                     row in COUNTRY_DB that contains the correct city
    """
    # gdfs of rows where city/country names are in their respective databases
    _city_gdf_rows      = CITY_DB   [CITY_DB.alt_names.apply   (lambda row: city_name    in row)]
    _country_gdf_rows   = COUNTRY_DB[COUNTRY_DB.alt_names.apply(lambda row: country_name in row)]

    # Length of extracted rows from databases
    n_cities_extracted    = len(_city_gdf_rows)
    n_countries_extracted = len(_country_gdf_rows)

    assert(n_cities_extracted > 0), \
          f'Unable to find {city_name}!'
    
    assert(n_countries_extracted > 0), \
          f'Unable to find {country_name}!'

    assert(n_countries_extracted == 1), \
          f'Found too many countries matching {country_name}!'
    
    # If multiple cities with that name
    if n_cities_extracted > 1:
        # From list of countries containing city_name, find the one that matches the country_name
        possible_countries    = set(_city_gdf_rows.country.to_list())
        allowable_countries   = set(_country_gdf_rows.alt_names.values[0])
        overlapping_countries = list(possible_countries.intersection(allowable_countries))

        assert(len(overlapping_countries) > 0), \
            f'No country {country_name} found for city {city_name}'

        # Extract correct row from remaining cities df
        overlapping_country = overlapping_countries[0]
        _city_gdf_rows      = _city_gdf_rows[_city_gdf_rows.country == overlapping_country]

    # By this stage, _city_gdf_rows should both just be one row _country_gdf_rows 
    # Amend country name in _city_gdf_rows to be the same as the primary name in _country_gdf_rows
    # As it stands, it could still be one of the country's alt_names
    if _city_gdf_rows.country.values[0] != _country_gdf_rows.name.values[0]:
        idx = _city_gdf_rows.index[0]
        print(f"Changed {city_name}'s country from \"{_city_gdf_rows.country.values[0]}\" to \"{_country_gdf_rows.name.values[0]}\"")
        _city_gdf_rows.at[idx, 'country'] = _country_gdf_rows.name.values[0]


    return _city_gdf_rows, _country_gdf_rows



# Initialise databases for importing into other sections
CITY_DB    = reduce_city_data('data/cities.csv')
COUNTRY_DB = reduce_country_data('data/countries.csv')