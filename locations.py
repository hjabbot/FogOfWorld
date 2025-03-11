import shapely
import numpy as np

from database import CITY_DB, COUNTRY_DB

class City:
    """
    Stores information about a single city, including name, country, and coordinates
    """
    def __init__(self, name, country=None, coords=None):
        self.name = name

        self._gdf_row = CITY_DB[CITY_DB.name == name]
        assert(len(self._gdf_row) == 1)


        # Retrieve country from database if none provided
        if country is None: self.country = Country(self._gdf_row.country)
        else:               self.country = country

        # Retrieve coordinates from database if none provided
        if coords is None: self.set_coords(name)
        else:              self.coords = coords

    def set_coords(self, name):
        pass

    @property
    def point(self):
        return shapely.Point((self.coords.lon, self.coords.lat))
    
    def __str__(self):
        return f'{self.name}, {self.country} {self.coords}'

class Country:
    """
    Stores information about a single country, including name and shape
    """
    def __init__(self, name, shape=None):
        self.name = name


        self._gdf_row = COUNTRY_DB[COUNTRY_DB.name == name]
        assert(len(self._gdf_row) == 1)


        # Retrieve country shape from database if none provided
        if shape is None:   self.set_shape(name)
        else:               self.shape = shape

    def set_shape(self, name):
        pass

    def __str__(self):
        return f'{self.name}'

    
class Terminator:
    """
    Stores information about the day/night terminator. Calculates all based on time measured in UTC
    """
    def __init__(self, time):
        self.time = time

    @property
    def sun_ecliptic_position(self):
        """
        Calculates the position of the sun in ecliptic coordinates

        Returns:
            (float, float): (lambda_e, radius_e) coordinates of sun
        """
        lon = (280.460 + 0.9856474 * self.time.mjd) % 360    # Mean Longitude of sun
        g = (357.528 + 0.9856003 * self.time.mjd) % 360      # Mean anomaly of sun

        # Ecliptic longitude of sun
        lambda_e = lon + 1.915 * np.sin(np.radians(g)) + 0.02 * np.sin(2 * np.radians(g))
        # Distance from sun in AU
        r_e = 1.00014 - 0.01671 * np.cos(np.radians(g)) - 0.0014 * np.cos(2 * np.radians(g))

        return (lambda_e, r_e)
    
    @property
    def ecliptic_obliquity(self):
        """
        Calculates the obliquity of the sun from modified julian date

        Returns:
            float: Sun obliquity
        """
        T = self.time.mjd / 36525    # Number of centuries since J2000

        epsilon = 23.43929111 - T * (46.836769 / 3600 - T * (0.0001831 / 3600 + T * (0.00200340 / 3600 - T * (0.576e-6 / 3600 - T * 4.34e-8 / 3600))))

        return epsilon
    

    @property
    def sun_equatorial_position(self):
        """
        Calculates the position of the sun above the earth in equitorial coordinates

        Returns:
            (float, float): Equitorial position of the sun
        """
        sun_ecliptic_lon = self.sun_ecliptic_position[0]

        alpha = np.degrees(np.arctan (np.cos(np.radians(self.ecliptic_obliquity))))* (np.tan(np.radians(sun_ecliptic_lon)))
        delta = np.degrees(np.arcsin (np.sin(np.radians(self.ecliptic_obliquity))  *  np.sin(np.radians(sun_ecliptic_lon))))

        l_quadrant = np.floor(sun_ecliptic_lon/90) * 90
        r_quadrant = np.floor(alpha/90) * 90

        alpha = alpha + l_quadrant - r_quadrant

        return (alpha, delta)

    
    @property
    def _coords(self):
        """
        Calculates the coordinates of the day/night terminator based off of the sun's current equitorial position

        Returns:
            list: (lon, lat) coordinates marking the boundary of the terminator
        """

        lon = np.arange(-180, 181, 1)

        alpha, delta = self.sun_equatorial_position

        ha = (self.time.gmst + lon/15) * 15 - alpha

        lat = np.degrees(np.arctan(-np.cos(np.radians(ha)) / np.tan(np.radians(delta))))

        return [(lon[i], lat[i]) for i in range(len(lon))]
    
    @property
    def polygon(self):
        """
        Terminator coordinates represented as a shapely polygon

        Returns:
            shapely.Polygon: Shape of night side of Earth
        """
        coords = self._coords
        coords += [coords[0]]   # Close the polygon by adding the first point to the end
        return shapely.Polygon(coords[::-1])
    