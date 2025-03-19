import shapely
import datetime

class Position:
    """
    Stores coordinates with lat/lon labels
    """
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f'({self.lon},{self.lat})'
    
    @property
    def point(self):
        return shapely.Point(self.lon, self.lat)
    

class Time:
    """
    Sets up easy access variables all based on a given time
    """
    def __init__(self, time=None):
        """
        Args:
            time (int, optional): 
                Timestamp; i.e. seconds since 1 Jan 1970. Defaults to current time.
                Easiest way to input is to use datetime: time = datetime.datetime(year, month, day).timestamp()
                Assumes inputting time as UTC
        """
        if time is None:
            self.time = int(datetime.datetime.now(datetime.UTC).timestamp())
        else:
            self.time = time
        
    @property
    def julian_day(self):
        """
        Returns time in julian days
        """
        return (self.time / 86400 + 2440587.5)
    @property
    def jd(self):
        """
        Alias for self.julian_day
        """
        return self.julian_day
    
    @property
    def modified_julian_day(self):
        """
        Returns time in modified julian days (J2000 epoch)
        """
        return self.julian_day - 2451545.0
    @property
    def mjd(self):
        """
        Alias for self.modified_julian_day
        """
        return self.modified_julian_day
    
    @property
    def gmst(self):
        """
        Returns Greenwich Mean Sidereal Time
        """
        return (18.697374558 + 24.06570982441908 * self.mjd) % 24